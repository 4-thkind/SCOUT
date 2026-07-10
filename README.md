# Universal Commerce Agent — Backend Model

> AI-powered cross-platform shopping assistant for India.  
> Searches Amazon, Flipkart, Blinkit, Zepto, Instamart, Myntra & Ajio simultaneously,  
> ranks results by a composite scoring engine, and streams an AI-generated recommendation.

---

## Architecture Overview

```
User Message (natural language)
        │
        ▼
  IntentRouter (Claude)         ← classifies into 6 intent types
        │
  ┌─────┴──────────────────────────────────────┐
  │ shopping_query / quick_commerce / price_check│
  └─────────────────────────────────────────────┘
        │
  IntentExtractor (Claude)      ← NL → structured JSON (budget, brand, features…)
        │
  ProductSearchTool             ← parallel fan-out to all platforms
  ┌─────┼──────────────────────────────────┐
  │     │     │      │      │      │       │
Amazon Flipkart Blinkit Zepto Instamart Myntra SerpAPI
  └─────┴──────────────────────────────────┘
        │ List[Product] (deduplicated)
        │
  ProductRanker                 ← multi-factor scoring (price fit, rating, delivery…)
        │
  ReviewSummarizer (Claude)     ← pros/cons/verdict per product (concurrent)
        │
  SSE Stream ──────────────────► Frontend
   ├── THINKING events (loading badges)
   ├── INTENT event (parsed intent echo)
   ├── PRODUCTS event (ranked product cards)
   └── TEXT tokens (streaming AI narration)
```

---

## Key Design Decisions

| Problem in ShoppingGPT | Solution in this model |
|---|---|
| Global `ConversationBufferMemory` shared by ALL users | Per-session `Session` objects, UUID-keyed, Redis or local TTL-cache |
| TF-IDF keyword router — breaks on Hindi/Hinglish | LLM (Claude) intent router — handles any language |
| Flask sync request/response | FastAPI async + SSE streaming |
| Hardcoded `E:\chatbot\...` Windows paths | `pydantic-settings` from environment variables |
| SQLite local product DB | Multi-platform API integrations with caching |
| No deduplication across platforms | Title-fingerprint deduplication |
| No product scoring / ranking | 6-factor weighted scoring engine |
| No review summarisation | Claude-powered per-product pros/cons |
| Single HTTP response (no streaming) | Server-Sent Events from first token |

---

## Quick Start

```bash
# 1. Clone and install
git clone <your-repo>
cd universal-commerce-agent
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Configure API keys
cp .env.example .env
# Edit .env — add your GEMINI_API_KEY and SERP_API_KEY at minimum

# 3. Run
python run.py
# → http://localhost:8000
# → http://localhost:8000/docs  (interactive API docs)
# → http://localhost:8000/api/health  (check which platforms are configured)
```

---

## API Reference

### POST /api/chat  (SSE streaming)

```json
Request:
{
  "message": "best wireless headphones under ₹3000",
  "session_id": "abc123",   // optional — server creates one if omitted
  "pincode": "110001"       // optional — for quick commerce delivery ETAs
}

SSE Events:
  event: thinking  → { "data": { "message": "Searching across platforms…" } }
  event: intent    → { "data": { "query_text": "wireless headphones", "budget_max": 3000, … } }
  event: products  → { "data": { "products": [...ProductCard], "platforms_searched": [...] } }
  event: text      → { "data": "Best pick is…" }   (token-by-token)
  event: done      → { "session_id": "abc123" }
```

### GET /api/search  (non-streaming)

```
GET /api/search?q=wireless+headphones&budget=3000&pincode=110001&sort=best_value
```

### GET /api/health

```json
{
  "status": "ok",
  "llm_connected": true,
  "platforms_configured": ["serp", "amazon", "flipkart"],
  "cache_connected": false
}
```

---

## Frontend Integration (Next.js example)

```typescript
// hooks/useChat.ts
export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [products, setProducts] = useState<ProductCard[]>([]);

  const sendMessage = async (text: string, sessionId?: string) => {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, session_id: sessionId }),
    });

    const reader = response.body!.getReader();
    const decoder = new TextDecoder();
    let aiText = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const lines = decoder.decode(value).split('\n');
      for (const line of lines) {
        if (!line.startsWith('data:')) continue;
        const chunk = JSON.parse(line.slice(5));

        if (chunk.type === 'text')     aiText += chunk.data;
        if (chunk.type === 'products') setProducts(chunk.data.products);
        if (chunk.type === 'done')     setMessages(m => [...m, { role: 'assistant', content: aiText }]);
      }
    }
  };

  return { messages, products, sendMessage };
}
```

---

## Adding a New Platform

1. Create `app/integrations/<platform>.py` extending `BaseIntegration`
2. Implement `async def search(intent, pincode) -> List[Product]`
3. Add to `_ECOMMERCE_PLATFORMS` or `_QUICK_COMMERCE_PLATFORMS` in `product_search.py`
4. Add API key fields to `app/config.py` and `.env.example`

---

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GEMINI_API_KEY` | Claude API key | ✅ Yes |
| `SERP_API_KEY` | SerpAPI key for Google Shopping | ✅ Day 1 |
| `AMAZON_ACCESS_KEY` / `SECRET_KEY` / `PARTNER_TAG` | Amazon PA-API 5.0 | ✅ Week 1 |
| `FLIPKART_AFFILIATE_ID` / `TOKEN` | Flipkart Affiliate API | ✅ Week 1 |
| `BLINKIT_API_KEY` / `BASE_URL` | Blinkit (via partnership) | 🔜 Future |
| `ZEPTO_API_KEY` / `BASE_URL` | Zepto (via partnership) | 🔜 Future |
| `INSTAMART_API_KEY` / `BASE_URL` | Swiggy Instamart | 🔜 Future |
| `REDIS_URL` | Redis for caching + sessions | Optional |

---

## Project Structure

```
app/
├── main.py                  FastAPI app factory
├── config.py                All settings from environment
├── agent/
│   ├── core.py              CommerceAgent — main orchestrator
│   ├── router.py            LLM intent classifier
│   └── prompts.py           All system prompts (single source of truth)
├── tools/
│   ├── intent_extractor.py  NL → structured SearchIntent
│   ├── product_search.py    Parallel multi-platform search
│   ├── product_ranker.py    6-factor scoring engine
│   ├── review_summarizer.py Claude-powered pros/cons
│   └── price_analyzer.py   Cross-platform price comparison
├── integrations/
│   ├── base.py              Abstract base + retry logic
│   ├── serp_api.py          Google Shopping (day 1)
│   ├── amazon.py            Amazon PA-API 5.0
│   ├── flipkart.py          Flipkart Affiliate
│   ├── blinkit.py           ADD API HERE
│   ├── zepto.py             ADD API HERE
│   ├── instamart.py         ADD API HERE
│   └── myntra_ajio.py       Fashion platforms
├── models/
│   ├── product.py           Unified Product, ProductCard
│   ├── intent.py            SearchIntent
│   ├── session.py           Session, ChatMessage
│   └── response.py          API request/response shapes
└── services/
    ├── llm_service.py       Anthropic Claude wrapper (stream + JSON)
    ├── cache_service.py     Redis + in-memory fallback
    └── session_service.py   Per-user isolated sessions
```

---

*Built for the Universal Commerce Agent project. See `universal_commerce_agent_roadmap.md` for full project context.*

---
version: alpha
name: CJP-member-design-analysis
description: Cockroach Janata Party (cjpmember.in) — warm near-black canvas, single amber accent, bold sans-serif with italic emphasis words, pill-shaped everything.

colors:
  canvas-night: "#1a1208"
  canvas-night-soft: "#241a0e"
  canvas-paper: "#f7f3ea"
  canvas-light: "#ffffff"
  ink: "#1a1208"
  on-primary: "#ffffff"
  accent-warn: "#c98a2c"
  accent-warn-soft: "#e7c98a"
  hairline-on-dark: "#3a2f1f"
  hairline-on-light: "#e5ddc9"
  ink-mute: "#6b5f4a"
  badge-bg: "#2a2013"

typography:
  display-hero:
    fontFamily: "Inter, 'Helvetica Neue', Arial, sans-serif"
    fontSize: 64px
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: -0.5px
    note: "emphasis words rendered italic within an upright headline"
  display-lg:
    fontFamily: "Inter, sans-serif"
    fontSize: 40px
    fontWeight: 800
    lineHeight: 1.15
    letterSpacing: -0.3px
  display-md:
    fontFamily: "Inter, sans-serif"
    fontSize: 28px
    fontWeight: 700
    lineHeight: 1.25
  body-lg:
    fontFamily: "Inter, sans-serif"
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.6
  body-md:
    fontFamily: "Inter, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.55
  button-cap:
    fontFamily: "Inter, sans-serif"
    fontSize: 14px
    fontWeight: 600
    letterSpacing: 0.2px
  micro-cap:
    fontFamily: "Inter, sans-serif"
    fontSize: 12px
    fontWeight: 600
    letterSpacing: 1.2px
    textTransform: uppercase

rounded:
  xs: 4px
  sm: 8px
  md: 14px
  pill: 999px

spacing:
  xs: 8px
  sm: 12px
  md: 16px
  lg: 20px
  xl: 32px
  xxl: 48px
  huge: 80px

components:
  button-primary-cta:
    backgroundColor: "{colors.accent-warn}"
    textColor: "{colors.canvas-night}"
    typography: "{typography.button-cap}"
    rounded: "{rounded.pill}"
    padding: 14px 24px
  button-secondary-outline:
    backgroundColor: "transparent"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-cap}"
    rounded: "{rounded.pill}"
    padding: 14px 24px
  badge-pill:
    backgroundColor: "{colors.badge-bg}"
    textColor: "{colors.accent-warn-soft}"
    typography: "{typography.micro-cap}"
    rounded: "{rounded.pill}"
    padding: 6px 14px
  card-dark:
    backgroundColor: "{colors.canvas-night-soft}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 20px
  card-paper:
    backgroundColor: "{colors.canvas-paper}"
    textColor: "{colors.ink}"
    typography: "{typography.display-md}"
    rounded: "{rounded.sm}"
    padding: 32px
  nav-bar-fixed:
    backgroundColor: "{colors.canvas-night}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-cap}"
    rounded: "{rounded.xs}"
    padding: 16px 32px
  chip-pill:
    backgroundColor: "{colors.badge-bg}"
    textColor: "{colors.on-primary}"
    typography: "{typography.micro-cap}"
    rounded: "{rounded.pill}"
    padding: 8px 16px
---

## Key Rules
- **Canvas:** warm near-black `{colors.canvas-night}` (#1a1208) — NOT pure `#000000`. Reads like burnt kraft paper, not dark-mode UI.
- **One accent only:** `{colors.accent-warn}` amber/gold, used ONLY on primary CTAs and small badge text. Never as a background fill or body text color.
- **Font:** Inter (or Helvetica Neue / system-ui fallback), bold/heavy weights (700–800) for all display type. No serif, no condensed fallback.
- **Signature move:** headlines mix upright + italic weight on the same line for emphasis (e.g. one or two key words go italic, rest stays upright).
- **Shape:** every button, badge, and chip is full pill radius (`{rounded.pill}` = 999px). Cards use 8–14px radius, never sharp corners.
- **One light break:** the page is dark almost everywhere; exactly one section flips to `{colors.canvas-paper}` (warm off-white) for contrast — don't overuse light cards.
- **Numbered structure:** any list (manifesto, requirements) uses numeral prefixes (`01`, `02`...) to feel like a formal document, not marketing bullets.

## Type Scale
| Token | Size | Weight | Line Height | Use |
|---|---|---|---|---|
| `display-hero` | 64px | 800 | 1.05 | Hero headline |
| `display-lg` | 40px | 800 | 1.15 | Section headers |
| `display-md` | 28px | 700 | 1.25 | Sub-heads / quotes |
| `body-lg` | 18px | 400 | 1.6 | Lead paragraphs |
| `body-md` | 16px | 400 | 1.55 | Default body |
| `button-cap` | 14px | 600 | 1.0 | Buttons |
| `micro-cap` | 12px | 600 | 1.4 | Badges / eyebrows (uppercase) |

## Do
- Warm dark canvas + single amber accent, disciplined use.
- Pill shape on every interactive element.
- Italic emphasis words in headlines.

## Don't
- Don't use pure black.
- Don't spread the accent color across multiple elements per section.
- Don't use more than one light/paper-toned section per page.

**Confidence note:** colors/fonts inferred from the confirmed `theme-color` meta (`#1a1208`) + Next.js/Inter conventions, not pixel-extracted CSS. Pull DevTools computed styles if you need exact hex/font values.

## Prompts (feed these to another agentic AI along with this file)

### Master prompt — build a new page/site using this system
```
Here is a DESIGN.md handfile describing a design system. Use it as the single source of truth for every visual decision — colors, fonts, spacing, radius, and component styling must all come from the tokens in this file, not from your own defaults.

Rules:
- Always reference tokens by name (e.g. {colors.accent-warn}, {rounded.pill}) instead of inventing new hex codes or sizes.
- Follow the "Key Rules" and "Do / Don't" sections exactly — they are non-negotiable constraints, not suggestions.
- Match the Type Scale table for every text element — pick the closest token, don't freehand font sizes.
- If something isn't covered in the file (e.g. a component type that doesn't exist yet), infer it in the same visual language and stay consistent — warm near-black canvas, single amber accent, pill shapes, Inter bold display type.

Now build: [describe what you want — e.g. "a pricing page", "a landing page hero + 3-feature section", "a signup form"]
```

### Component-specific prompt
```
Using the attached DESIGN.md, build a [component name — e.g. "navbar", "hero section", "card grid"] that strictly follows:
- canvas-night (#1a1208) as background, never pure black
- accent-warn used only on the primary CTA / badge, nowhere else
- Inter font, 700-800 weight for any heading
- pill radius (999px) on every button/badge/chip
- numbered prefixes if this is a list/steps component

Output clean HTML/CSS (or [React/Tailwind/etc. — specify your stack]) using the exact token values from the file.
```

### Quick single-line prompt (for fast iteration)
```
Follow DESIGN.md strictly — warm near-black canvas, one amber accent only, Inter bold headlines with italic emphasis words, everything pill-shaped. Build: [your request]
```

### Consistency-check prompt (use after the AI generates something)
```
Check what you just built against DESIGN.md's "Do" and "Don't" lists. Fix any violations — especially: pure black instead of #1a1208, accent color used in more than one place per section, sharp corners instead of pill radius, or missing italic emphasis in headlines.
```

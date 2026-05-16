---
name: yasashii-frontend
description: Redesign the Yasashii Sensei web frontend with a modern magical Japanese aesthetic using Tailwind CSS, subtle animations, and a dark elegant theme
---

Redesign the Yasashii Sensei frontend with a distinctive,
production-grade aesthetic. Avoid generic AI aesthetics.

## Design Direction: "Midnight Tokyo"

**Concept**: Dark, elegant, magical — like reading Japanese 
poetry under city lights at night. The UI should feel like 
a premium language learning experience, not a generic web app.

**Tone**: Refined dark luxury with subtle Japanese cultural elements.
Think: ink on paper, sakura at night, neon reflections on wet streets.

**The ONE unforgettable thing**: Japanese characters that 
shimmer/glow when the analysis completes — like ink appearing 
on paper.

---

## Technical Stack

- **Tailwind CSS** via CDN — use utility classes throughout
- **Vanilla JS** — no framework needed
- **Google Fonts**: 
  - `Noto Serif JP` for Japanese text (elegant, authentic)
  - `DM Sans` for UI elements (modern, clean)
- **CSS animations** — subtle, purposeful, not distracting
- **Flask Jinja2 templates** — must work with Flask

---

## Color Palette (CSS Variables)

```css
:root {
  --bg-primary: #0a0a0f;        /* near black */
  --bg-secondary: #12121a;      /* dark navy */
  --bg-card: #1a1a26;           /* card background */
  --bg-elevated: #22223a;       /* elevated elements */
  --accent-primary: #7c6fe0;    /* soft purple */
  --accent-sakura: #e879a0;     /* sakura pink */
  --accent-gold: #f0c85a;       /* gold for JLPT */
  --accent-jade: #4ade80;       /* jade green */
  --text-primary: #f0f0f8;      /* near white */
  --text-secondary: #9090b0;    /* muted */
  --text-tertiary: #5050708;    /* very muted */
  --border: rgba(120, 120, 180, 0.15);
  --glow: rgba(124, 111, 224, 0.3);
}
```

---

## Typography

```css
/* Japanese text */
.jp-text {
  font-family: 'Noto Serif JP', serif;
  letter-spacing: 0.05em;
  line-height: 2;
}

/* UI elements */
body {
  font-family: 'DM Sans', sans-serif;
}
```

---

## Layout & Components

### Header
Use the pre-generated banner image as the header:
- Image path: /static/images/header-banner.png
- Full width, responsive
- Max height: 200px on desktop, 120px on mobile
- object-fit: cover, object-position: center
- Subtle overlay: linear-gradient(to bottom, 
  transparent 60%, var(--bg-primary) 100%)
  so it blends into the dark background below
- No additional text needed — banner already has 
  やさしい先生 and "Your Gentle Japanese Teacher"
- Slight fade-in animation on page load

### Hero/Input Section
```
Large, centered input area
Dark card with subtle border glow on focus
Two tab buttons: 
  - 「NHK Web Easy」 
  - 「Paste Text」
Styled with Japanese bracket characters
Analyze button: gradient from purple to sakura pink
Subtle pulse animation on button hover
```

### Article Cards
```
Dark cards with left border accent in sakura pink
JLPT badge: colored pill (N5=jade, N4=blue, N3=yellow, N2=orange, N1=red)
Topic tag: subtle ghost pill
Hover: card lifts with glow effect
```

### Results Page
```
Original text display:
- Large Noto Serif JP font
- Subtle ink-reveal animation on load (opacity + slight y transform)
- JLPT badge top right with glow

Vocabulary cards:
- Dark grid cards
- Japanese word large, reading small above in muted color
- Meaning below
- Hover: purple border glow

Grammar section:
- Left border accent in gold
- Pattern in purple monospace font
- Explanation in regular text

Cultural notes:
- Special styling — slightly different background
- Gold left border
- Feels like a footnote from an ancient text

🔊 Listen button:
- Pill shaped, purple gradient
- Ripple animation on click
- Loading spinner while fetching audio
```

---

## Animations

```css
/* Ink reveal — for original text appearing */
@keyframes inkReveal {
  from { opacity: 0; transform: translateY(8px); filter: blur(4px); }
  to   { opacity: 1; transform: translateY(0);   filter: blur(0); }
}

/* Glow pulse — for analyze button */
@keyframes glowPulse {
  0%, 100% { box-shadow: 0 0 20px var(--glow); }
  50%       { box-shadow: 0 0 40px var(--glow), 0 0 60px rgba(232,121,160,0.2); }
}

/* Card float — on hover */
@keyframes cardFloat {
  to { transform: translateY(-4px); box-shadow: 0 8px 30px var(--glow); }
}

/* Shimmer — for loading state */
@keyframes shimmer {
  from { background-position: -200% 0; }
  to   { background-position: 200% 0; }
}

/* Staggered reveal — for results sections */
.reveal { 
  animation: inkReveal 0.5s ease forwards;
  opacity: 0;
}
.reveal:nth-child(1) { animation-delay: 0.1s; }
.reveal:nth-child(2) { animation-delay: 0.2s; }
.reveal:nth-child(3) { animation-delay: 0.3s; }
.reveal:nth-child(4) { animation-delay: 0.4s; }
```

---

## Files To Create

### templates/base.html
- Dark background
- Import Tailwind CDN
- Import Google Fonts (Noto Serif JP + DM Sans)
- CSS variables
- All animation keyframes
- Subtle noise texture overlay on body

### templates/index.html extends base.html
- Full redesign of input section
- Japanese bracket styled tabs: 「NHK Web Easy」「テキスト入力」
- Gradient analyze button with glow
- Article cards with hover effects
- Loading skeleton with shimmer

### templates/results.html extends base.html
- Ink reveal animation on page load
- Original text with furigana ruby styling
- Vocabulary grid with hover glows
- Grammar section with gold accent
- Cultural notes with special treatment
- 🔊 Listen button with ripple effect
- Navigation back button

### static/css/style.css
- All CSS variables
- Custom component styles not covered by Tailwind
- Animation definitions
- Furigana/ruby text styling
- Scrollbar styling (dark, thin)
- Selection color (purple)

### static/js/app.js
- All existing functionality preserved
- Add staggered reveal on results load
- Add ripple effect on buttons
- Add smooth tab transitions
- Typing animation for loading state

---

## Critical Rules

- NEVER use white or light backgrounds
- NEVER use generic purple gradient on white (cliché)
- ALL Japanese text uses Noto Serif JP
- Tailwind utility classes for layout/spacing
- Custom CSS only for animations and special effects
- Must work with Flask Jinja2 (no build step)
- API endpoints unchanged: /api/articles, /api/analyze, /api/tts
- Preserve ALL existing functionality
- Mobile responsive
- NO emojis anywhere in the UI — use elegant typography 
  and CSS instead of emoji icons
- Use unicode symbols sparingly if needed: ◆ ▸ — · 
- All buttons use English labels
- Listen button: "Listen"
- Analyze button: "Analyze"
- Tab labels: "NHK Web Easy" and "Paste Text"
- Navigation: "Back", "Home", "Browse Articles"
- Only Japanese text that appears is the actual 
  lesson content — never UI labels
  - Use Lucide icons via CDN (unpkg.com/lucide@latest)
- Icons accompany text labels — never replace them
- Icon size: 16px for inline, 20px for buttons
- Icon color matches text color
- Call lucide.createIcons() at bottom of body

---

## The Unforgettable Moment

When analysis results load — the original Japanese text
should appear with the ink reveal animation,
as if being written on paper in real time.

This is the moment judges will remember.
Execute it with precision.
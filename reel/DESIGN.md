# DESIGN — "Case File" reel

Visual identity for the 10s talking-head reel (`prachi-original-first-10s.mp4`).
Derived from the footage: warm cream study, dusty-rose blazer, wooden desk, soft window light.
The topic (visa rejection, "one document", "rejection letter") suggests paperwork — so the
graphic language is **editorial paperwork**: paper sheets, a rubber stamp, hairline rules,
typewriter-mono labels. Restrained, warm, no neon, no gradients.

## Palette (only these)

| Role    | Hex       | Use                                                          |
| ------- | --------- | ------------------------------------------------------------ |
| Ink     | `#1D1613` | caption shadow, card text/bars, scrims (never pure black)    |
| Paper   | `#F5EEE4` | caption text, paper cards (never pure white)                 |
| Stamp   | `#B8392A` | the single accent: stamp, underline sweep, marker ring       |
| Dust    | `#CDBFAE` | secondary labels, hairlines, inactive caption words          |

## Type

- **Archivo** (variable, local woff2) — captions & labels. Captions 800 weight, width 108%,
  sentence case, tracking -0.02em. Stamp text 900, width 125%, uppercase, +0.08em.
- **Instrument Serif Italic** (local woff2) — emphasis words only ("document", "why",
  "rejection letter"). Mixed into caption lines at ~1.3× size. This serif/sans tension is the
  voice shift from statement → consequence.
- **IBM Plex Mono** (bundled) — tiny file labels / metadata only, uppercase, +0.14em.

## Layout (1080×1920, Reels safe zones)

- Keep clear: top 220px, bottom 400px, right 120px (platform UI).
- Captions: centred block, zone y≈1180–1420, max-width 900px.
- Subject's face (source ≈ x570 y610) is never covered by type or cards.
- Header tag: top-left at y≈250, left margin 72px.

## Motion

- Camera: inner wrapper scale/pan only, origin on the face. Punches land on stressed words
  (0.12–0.18s, `expo.out`), everything else drifts slowly (`sine.inOut`/`none`).
- Captions: phrase groups of 1–4 words, words rise + fade in on their timestamp, karaoke from
  Dust → Paper; emphasis words break the pattern (serif, stamp, underline).
- One accent move per phrase at most. No bounce/elastic, no emoji, no glow.
- Sound-aware: header level meter and a ≤3% active-word lift driven by the voice RMS.

## Texture & depth

- Footage: left ungraded. `media-treatment --analyze` found no technical imbalance; the
  Natural Portrait candidate (`skin-soft` 0.55) was only marginally different and cost ~26s/frame
  under software WebGL, so the source's warm light stands as-is.
- Soft ink scrim behind the caption zone (bottom-up, ≤45%) for legibility.
- Paper cards: 4px corner radius, one soft ink shadow, faint ruled lines.

## Don'ts

- No gradient text, no neon, no pure #000/#fff, no emoji, no extra claims or CTA text
  beyond the spoken dialogue.
- No more than one moving graphic besides captions at any moment.

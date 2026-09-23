# Custom asset prompts

Every scene already works with clean built-in icons. Each asset below is an **optional upgrade**:
save it as `assets/custom/<file>.png`, run `python tools/build.py`, and the scene swaps it in
automatically. No other change is needed.

**Background:** generate on a plain white or light-grey background. I cut it out with
`npx hyperframes remove-background <file> -o assets/custom/<file>.png`, so you don't need to
make it transparent.

**Size:** square, 2048×2048 (1024 minimum). One object, centred, with about 12% empty margin on
every side.

## Style block (paste in front of every prompt)

> Premium 3D icon render, single object, soft matte-clay material with a subtle satin sheen,
> rounded bevelled edges, studio softbox key light from the top-left, soft fill, thin cool rim
> light, gentle ambient occlusion, very slight three-quarter view (about 20° yaw, 10° tilt),
> centred, plain seamless light-grey background, no cast shadow on the background, crisp clean
> edges, high detail, product-render quality. Colour palette only: ink #15121A, off-white #FBFBF6,
> lemon #F6F97F, alarm red #FF2E3F, navy #1C2442. No text, no letters, no numbers, no logos, no
> flags, no watermark.

**Negative prompt** (for tools that take one): text, letters, words, numbers, logo, watermark,
flag, national emblem, hands, people, clutter, multiple objects, harsh shadow, cartoon outline,
low poly, noise, blurry.

The palette and lighting are what make the set look like one family. If a result drifts off
palette, regenerate it rather than recolouring it.

## Assets

| # | File | Used in (source time) | Prompt (after the style block) |
| - | ---- | --------------------- | ------------------------------ |
| 1 | `passport.png` | 0.0–1.9s "Your visa got **rejected**" (icon on the visa-application card) | A closed passport booklet with a deep navy leather-textured cover, a simple embossed circular globe motif in soft gold-cream in the centre, softly rounded corners, a slight page-block thickness visible on one edge. No text or country emblem. |
| 2 | `document.png` | 2.0–4.4s "this **one document**" (lemon tiles) and 22.2–24.6s "**a hundred times**" (the 100-copy grid) | A single sheet of off-white paper standing slightly angled, top-right corner folded over, a few thin ink-grey text lines suggested as simple raised bars (not real text), a small navy bar at the top like a header. |
| 3 | `envelope.png` | 8.0–9.6s "the **rejection letter arrives**" (notification app icon, shown on a red tile) | An off-white paper envelope, flap open, the top edge of a folded letter peeking out, one small alarm-red circular wax seal on the flap. |
| 4 | `icon-goals.png` | 18.0s "**generic goals**" | A dartboard-style target in off-white and ink rings with a single dart that missed and hangs off the outer ring, dart fletching in alarm red. |
| 5 | `icon-copy.png` | 19.2s "**copied lines**" | Two identical off-white paper sheets overlapping and offset, with a curved arrow between them like a duplicate/copy symbol, the arrow in alarm red. |
| 6 | `icon-story.png` | 20.5s "**zero personal story**" | A simple rounded bust silhouette (head and shoulders, no face features) in off-white next to an empty speech bubble drawn with a dashed alarm-red outline. |
| 7 | `icon-country.png` | 29.7s "why this **country**" (tile 1 flips to it) | A small glossy globe on a short stand, continents as soft raised shapes in lemon #F6F97F on an ink #15121A sphere. No real map labels. |
| 8 | `icon-course.png` | 31.0s "why this **course**" (tile 2) | A graduation mortarboard cap in ink #15121A with a lemon #F6F97F tassel, resting on a closed book. |
| 9 | `icon-now.png` | 32.1s "why **now**" (tile 3) | A round stopwatch in ink #15121A with a lemon #F6F97F face and a single hand, crown button on top. No numbers. |
| 10 | `icon-review.png` | 42.8s "**free SOP reviews**" (consultancy card stack) | An off-white paper sheet with a lemon magnifying glass resting on it at an angle, the lens showing a small ink check mark. |
| 11 | `icon-calendar.png` | 44.0s "**this month**" (consultancy card stack) | A tear-off desk calendar block, off-white pages, ink binding rings, a lemon header band, a blank date area (no numbers). |
| 12 | `logo.png` (optional, **not AI**) | 41.1–44.7s "Work Abroad Consultancy" | Send the consultancy's real logo if they have one (PNG or SVG). I won't generate a logo for a real business. |

## Why icons and not photoreal props

The scenes you liked (past → future line, the DM composer, the "why" badges) are clean, flat UI
driven by the dialogue. The ones that read as cheap were fake-real paper pasted over her. So every
scene now follows one rule: blur the footage, put one crisp object and the spoken words centre
stage, then hand back to her face. 3D icons in one consistent style fit that rule; photoreal props
would bring back the pasted-on look.

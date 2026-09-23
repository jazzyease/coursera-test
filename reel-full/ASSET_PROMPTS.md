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
> lime #E6F54A, alarm red #FF2E3F, navy #1C2442. No text, no letters, no numbers, no logos, no
> flags, no watermark.

**Negative prompt** (for tools that take one): text, letters, words, numbers, logo, watermark,
flag, national emblem, hands, people, clutter, multiple objects, harsh shadow, cartoon outline,
low poly, noise, blurry.

The palette and lighting are what make the set look like one family. If a result drifts off
palette, regenerate it rather than recolouring it.

## Assets

| # | File | Used in (source time) | Prompt (after the style block) |
| - | ---- | --------------------- | ------------------------------ |
| 1 | `passport.png` | 0.0–1.9s "Your visa got **rejected**" (visa status card) | A closed passport booklet with a deep navy leather-textured cover, a simple embossed circular globe motif in soft gold-cream in the centre, softly rounded corners, a slight page-block thickness visible on one edge. No text or country emblem. |
| 2 | `document.png` | 2.0–4.4s "this **one document**" and 22.2–24.6s "**a hundred times**" | A single sheet of off-white paper standing slightly angled, top-right corner folded over, a few thin ink-grey text lines suggested as simple raised bars (not real text), a small lime square in the top-left corner like a header mark. |
| 3 | `envelope.png` | 8.0–9.6s "the **rejection letter arrives**" (notification) | An off-white paper envelope, flap open, the top edge of a folded letter peeking out, one small alarm-red circular wax seal on the flap. |
| 4 | `icon-goals.png` | 18.0s "**generic goals**" | A dartboard-style target in off-white and ink rings with a single dart that missed and hangs off the outer ring, dart fletching in alarm red. |
| 5 | `icon-copy.png` | 19.2s "**copied lines**" | Two identical off-white paper sheets overlapping and offset, with a curved arrow between them like a duplicate/copy symbol, the arrow in alarm red. |
| 6 | `icon-story.png` | 20.5s "**zero personal story**" | A simple rounded bust silhouette (head and shoulders, no face features) in off-white next to an empty speech bubble drawn with a dashed alarm-red outline. |
| 7 | `icon-check.png` | 28.2s "a **strong SOP** answers three things" | A glossy rounded-square badge in lime #E6F54A with a thick ink #15121A check mark, slightly raised like a button. |
| 8 | `icon-review.png` | 42.8s "**free SOP reviews**" (brand card) | An off-white paper sheet with a lime magnifying glass resting on it at an angle, the lens showing a small ink check mark. |
| 9 | `icon-calendar.png` | 43.9s "**this month**" (brand card) | A tear-off desk calendar block, off-white pages, ink binding rings, a lime header band, a blank date area (no numbers). |
| 10 | `logo.png` (optional, **not AI**) | 41.1–44.7s "Work Abroad Consultancy" | Send the consultancy's real logo if they have one (PNG or SVG). I won't generate a logo for a real business. |

## Why icons and not photoreal props

The scenes you liked (past → future line, the DM composer, the "why" badges) are clean, flat UI
driven by the dialogue. The ones that read as cheap were fake-real paper pasted over her. So every
scene now follows one rule: blur the footage, put one crisp object and the spoken words centre
stage, then hand back to her face. 3D icons in one consistent style fit that rule; photoreal props
would bring back the pasted-on look.

# DESIGN — "Creator Punch" reel (v2)

Style is taken from the four reference reels the user supplied (tubetactix, ManavSharma,
123faadkhan, luemmy21), applied to `prachi-original-first-10s.mp4`. v1 ("Case File", cream
editorial) was rejected by the user.

## What the references share

- Heavy **extended italic caps** at chest/desk height, two lines: line 1 white, line 2 in an
  accent colour with a soft glow (luemmy "IT TOOK ME / FOUR YEARS", tubetactix "INSTEAD OF /
  JUST SITTING THERE").
- Words **ghost in** (faint) then snap to full; accent lines slide in from the left.
- Moody, darker rooms with the speaker brighter than the background.
- **Colour moments**: the background flashes red behind the speaker (luemmy "SHOULD NOT"), the
  frame drops to black-and-white with red type (luemmy "DON'T EVER").
- **Yellow numbered circle badge** with glow (luemmy "1", "2", "3").
- **Glossy white UI cards** popping in over the torso (luemmy cards, tubetactix doc cards).
- **Blur transition** on a beat change (ManavSharma).
- Jump zooms between phrases, punch-ins on key words, lots of pop/whoosh/impact SFX.

## Palette (only these)

| Role   | Hex       | Use                                                   |
| ------ | --------- | ----------------------------------------------------- |
| Night  | `#0E0B10` | dim layer, text shadow, card text                     |
| White  | `#FBFBF6` | line-1 captions, UI cards                             |
| Lime   | `#E6F54A` | accent line, number badge, card highlight             |
| Alarm  | `#FF2E3F` | "REJECTED", "REJECTION LETTER", red flash, stamp      |
| Steel  | `#C9CBD3` | placeholder text lines on objects                     |
| Navy   | `#1B2340` / `#2A3458` | passport cover + cover edge               |
| Paper  | `#EFEBE1` / `#D9D5CC` | passport pages, sheets, envelope          |

## Type

- **Archivo Italic** (variable, local woff2): all captions and badges. 900 weight, width
  118%, uppercase, tracking -0.01em. Line 1 ≈ 80px; accent lines 84–156px (pre-sized to ≤940px).
- **JetBrains Mono** (bundled): passport machine-readable-zone chevrons only.

### Caption finish (v4 asked for gradient / glow / 3D depth; v5 toned it down to remove "AI slop")

Each word is three stacked layers of the same glyphs:
1. `::before`: short dark tone extrusion (4 stepped em-based shadows) plus a soft drop shadow.
2. Face: solid tone colour + a soft tone glow. This is the layer the contrast audit reads.
3. `::after`: vertical gradient fill clipped to the glyphs; hero words get one slow light pass.

| Tone  | Gradient (top → bottom)                     | Extrusion |
| ----- | ------------------------------------------- | --------- |
| White | `#FFFFFF` → `#F4F4EF` → `#D4D6DF` → `#B3B6C4` (chrome) | `#2B2731` |
| Lime  | `#FCFFD9` → `#F0FB8A` → `#E6F54A` → `#B5CD10` | `#3F4A04` |
| Red   | `#FFC2C9` → `#FF6674` → `#FF2E3F` → `#B50B22` | `#4D0610` |

Hero words ("REJECTED", "WHY", "ARRIVES") land with a short 1.28→1 scale, no overshoot.

## Layout (1080×1920)

- Captions: centred, block centre ≈ y1330 (desk/hands). Her white T-shirt sits at chest height, so
  captions go below it, not on it.
- 3D objects: centred at chest between chin and captions (≈ y800–1250). Checked at every
  camera punch so they never cover the mouth or chin.
- Safe zones: top 220px, bottom 380px, right 120px kept clear of key content.

## Footage treatment

- Background dimmed ~40% using the HyperFrames `remove-background` cutout (subject re-laid on
  top), so she stays bright like the references' lit speakers in dark rooms.
- Red flash: solid Alarm layer between the dimmed plate and the cutout.
- Hook: opens at 1.16× and settles out over 0.45s, so frame 0 is already moving (no roll).
- B&W and blur moments are ffmpeg-preprocessed variants of the source (`assets/media/`),
  cross-faded as layers. They're deterministic and cheap, with no shader cost.

## Motion

- Captions hard-swap between phrases (no fades), as in the references.
- Camera: jump zooms at phrase starts; 0.12–0.16s punches on "rejected" / "rejection"; slow
  push-ins in between; 3-frame shake on impacts. Origin = her face.
- Props (v5) are photoreal pre-renders from `tools/make_assets.py` (numpy/PIL, fixed seeds): paper
  grain + fibres, lit pebbled-leather cover, pastel guilloche security print, a hologram foil, fine
  print made of seeded pseudo-words (too small to read, so no invented copy), a curved-gutter bend,
  and a worn rubber-stamp ink texture. The passport photo is the subject herself (source frame at
  4.8s, cut out with `hyperframes remove-background`, greyscale). Field values are "XXXX" placeholders.
- `compositions/passport.html`, `doc-stack.html`, `envelope.html` place those PNGs in CSS 3D with
  a thin cover edge, a blurred contact shadow, and a soft-light sheen masked to the prop that
  follows the tilt. The stamp presses down (1.3→1 scale, 0.11s) and the prop gives 1.5%.
- Motion is a slow, low-amplitude drift (≤5px, ≤4° yaw). Camera shakes are 4–5px.
- Removed in v5 as exaggeration: god rays, bokeh, light streaks, caption haze, RGB-split glitch
  and glitch SFX, red strobe, ink splatter, shockwave rings and sparks, glowing halos, scan beam.

## Don'ts

- No invented claims, stats, logos or CTAs; only her spoken words appear as text.
- No emoji, no neon rainbow. Gradient text is allowed only in the three tone ramps above.

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
  118%, uppercase, tracking -0.01em. Line 1 ≈ 80px, line 2 ≈ 108px, hero words up to 156px.
- **JetBrains Mono** (bundled): passport machine-readable-zone chevrons only.

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
- B&W and blur moments are ffmpeg-preprocessed variants of the source (`assets/media/`),
  cross-faded as layers. They're deterministic and cheap, with no shader cost.

## Motion

- Captions hard-swap between phrases (no fades), as in the references.
- Camera: jump zooms at phrase starts; 0.12–0.16s punches on "rejected" / "rejection"; slow
  push-ins in between; 3-frame shake on impacts. Origin = her face.
- Motion graphics are JS-built CSS-3D objects (v3; the user rejected the flat SVG cards).
  One reusable sub-composition per story beat, each on its own local clock:
  - `compositions/passport.html`: open passport (cover thickness layers, hinged pages, generated
    guilloche security pattern, rotating foil seal). "REJECTED" stamp slams at 0.96s with ink
    splatter and a shockwave.
  - `compositions/doc-stack.html`: five sheets fan in, four fall away on "one", the chosen sheet
    comes forward with a glint + lime outline, a scan beam passes on "probably", and a marker ring
    draws on "why".
  - `compositions/envelope.html`: envelope spins in, the flap opens in 3D, the letter slides out,
    and the stamp slams with ink and a shockwave.
- Every object floats on layered sines (y / rotX / rotY / rotZ at different frequencies) with a
  sheen that follows the tilt. Canvas FX (ink, shockwave, sparks, marker) use a seeded PRNG and
  are drawn from one GSAP clock `onUpdate`, so every frame is reproducible and seek-safe.

## Don'ts

- No invented claims, stats, logos or CTAs; only her spoken words appear as text.
- No emoji, no gradient text, no neon rainbow.

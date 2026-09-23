# DESIGN: full reel (`prachi-full.mp4`, 50.8s source → 47.7s edit)

Extends the approved 10s cut in `../reel/` (its DESIGN.md is the base spec: palette, caption
finish, "no AI slop" rules). The first 9.5s here are the same hook, frame for frame.

## Scene system (v3: matched to the reference reels)

v2's centre-stage scenes over *blurred* footage still read as muddy. v3 follows what the
references actually do (studied frame by frame from luemmy21 / tubetactix):

- **Graphics on sharp footage at chest height** (y 700–1160, between chin and hands), with her face
  always visible: white cards stacked with a 14px gap (the user's reference frame), lemon tiles,
  a notification card, a ring.
- **Light cutaways** for the two "explain the object" beats: a cream → pale-lemon ground
  (sampled `#FDFFB6`) with a crisp white document window and ink-coloured type. Hard cut in and out.
- **One component kit** in `tools/scenes/_base.css`: `.wcard` (pure white, radius 26, one soft
  shadow), `.ltile` (lemon `#FEFFC4 → #F6F98A → #EDF164` with a pale `#FDFED2` bevel edge and soft
  glow, sampled from the "1 2 3" tiles), `.ground`, `.ink-cap`.
- **Captions re-finished to the reference**: heavy extended italic, flat bevel (white → cool
  grey), one tight dark shadow, no deep extrusion or glow; accent is lemon `#F6F97F`, not lime.
  Accent sizes are 80% of v2 (heroes ≤128px).
- No placeholder skeleton rows on any card: every card carries the spoken words or an icon.

| Source s | Line | Scene | Type |
| --- | --- | --- | --- |
| 0–1.9 | "Your visa got rejected" | `visa-status`: white "Visa application" card, pill goes from "In review ···" to red REJECTED; red backdrop behind her | chest card |
| 2.0–4.4 | "this one document is probably why" | `doc-pick`: five lemon document tiles, four drop; hand-drawn callout "THIS ONE." (as spoken); red "?" on "why" | chest tiles |
| 7.5–9.6 | "after the rejection letter arrives" | `letter`: notification card with stacked ghost lands and buzzes over the B&W frame | chest card |
| 9.56–12.5 | "It's called your statement of purpose" | `sop-title`: light cutaway, document window; heading set as spoken, initials marked in lemon, words clear and one "SOP" tile lands | cutaway |
| 16.6–21.8 | "A weak SOP has generic goals, copied lines, zero personal story" | `slabs-weak`: red "WEAK SOP" tab + three white cards, each struck through with a red ✕ at the end of its phrase | chest cards |
| 22.2–24.6 | "The officer has seen it a hundred times" | `hundred`: light cutaway, ink headline as spoken, one SOP then 99 identical copies, ×1 → ×100 | cutaway |
| 25.0–26.2 | "Instant red flag" | red backdrop behind her | face |
| 26.9–32.8 | "answers three things. Why this country / course / now" | `tiles-why`: lemon tiles 1 2 3 pop on "three things", each flips to its answer icon + label on its "why" (spans a jump cut; timed through the edit map) | chest tiles |
| 33.4–37.2 | "past to your future in one clean line" | `past-future` (kept, lemon recolour) | chest |
| 39.7–41.1 | "in the next 60 days" | `ring-60`: countdown ring fills as 0 → 60 | chest ring |
| 41.1–44.8 | "Work Abroad Consultancy… free SOP reviews this month" | `brand`: same white-card stack: name, "Free SOP reviews", "This month", each as spoken | chest cards |
| 45.5–48.0 | "DM the word SOP or hit the link in bio" | `dm` (kept, lemon recolour) | chest |
| 48.6–50.8 | "Don't let a fixable mistake cost you a year" | captions, slow push-in, 1.24s end freeze | face |

Custom assets: every icon slot has a built-in line icon. Dropping `assets/custom/<name>.png` in
place (prompts in `ASSET_PROMPTS.md`) swaps it in on the next `python tools/build.py`.

## Edit

- 9 jump cuts remove 4.28s of dead air between sentences (`tools/edit_map.py`). Each cut sits in
  measured silence (37–90 dB below speech); list pauses ("goals, copied lines, zero…") are kept.
- Framing alternates on every cut (wide ↔ tight, face-centred) so the cuts read as intentional.
  Punches only on stressed words: rejected, rejection, denied, red, now, That's it, 60.
- Voice is cut on the same segments as the picture; no music (none supplied).

## Layout notes (found in review)

- The hook's falling sheets fade as they drop so white paper never sits behind white captions.
- Multi-instance components must have the internal composition id and timeline key equal to the
  host id. A shared id (`sop` × 4) passed lint/check but silently blanked the plate video while
  any instance was on screen. Every scene template in `tools/scenes/` is therefore written out once
  per host by `tools/build.py`, with `__ID__` set to the host id.

## Palette additions

| Role | Hex | Use |
| --- | --- | --- |
| Red tint | `#FFE3E6` / `#E0162A` | icon discs on the weak-SOP cards |
| Lemon | `#F6F97F` (tiles `#FEFFC4→#EDF164`, edge `#FDFED2`) | replaces v2 lime `#E6F54A` everywhere |
| Ground | `#FDFFB6 → #FBFBF4` | light cutaways |
| Navy | `#1C2442` | brand card bar, tag, name |

## Build

```bash
npx hyperframes remove-background prachi-full.mp4 -o /tmp/subject-full.webm --quality best
tools/make_plate.sh /tmp/subject-full.webm   # dimmed-room plate, red-flag cutout, end-hold frame
python tools/build.py                        # index.html + every compositions/*.html from tools/scenes
npm run check && npm run render
```

Author in source seconds: `tools/build.py` (captions, camera, SFX, prop windows) and the
`compositions/*` variables. Each prop window sits inside one segment, so its local times are
source offsets.

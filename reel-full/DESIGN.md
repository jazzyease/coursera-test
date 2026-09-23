# DESIGN: full reel (`prachi-full.mp4`, 50.8s source → 47.7s edit)

Extends the approved 10s cut in `../reel/` (its DESIGN.md is the base spec: palette, caption
finish, "no AI slop" rules). The first 9.5s here are the same hook, frame for frame.

## Story → visuals (every visual is named in the dialogue)

| Source s | Line | Visual |
| --- | --- | --- |
| 0–9.5 | hook | passport stamp, document stack, envelope (unchanged); B&W from "rejection" |
| 9.56 | "It's called your statement of purpose" | colour returns; SOP page prop rises in |
| 12.2–16.0 | "…getting it wrong… visas get denied" | captions only; punch on "denied" |
| 16.7–21.7 | "A weak SOP has generic goals, copied lines, zero personal story" | same page, red pen per phrase: wavy underline, strike-through, boxed + crossed empty section |
| 22.3–24.5 | "seen it a hundred times" | identical copies fan out sideways behind the page |
| 25.0–26.2 | "Instant red flag" | red backdrop behind her (callback to the hook) |
| 26.9–29.2 | "A strong SOP answers three things" | the page returns clean; green tick drawn |
| 29.7–32.6 | "Why this country / course / now" | numbered badges 1–3 (luemmy21), framing tightens per question |
| 33.4–37.2 | "connects your past to your future in one clean line" | PAST ● and ● FUTURE nodes, one line drawn between them |
| 39.0–40.9 | "in the next 60 days" | "60" counts up |
| 41.2–44.8 | "Work Abroad Consultancy… free SOP reviews this month" | text-only lower-third card (no logo invented) |
| 45.5–48.0 | "DM the word SOP or hit the link in bio" | neutral message bar types "SOP", sends; "Link in bio" pill |
| 48.6–50.8 | "Don't let a fixable mistake cost you a year" | captions + slow push-in; 1.24s freeze on the last frame so the line can be read |

## Edit

- 9 jump cuts remove 4.28s of dead air between sentences (`tools/edit_map.py`). Each cut sits in
  measured silence (37–90 dB below speech); list pauses ("goals, copied lines, zero…") are kept.
- Framing alternates on every cut (wide ↔ tight, face-centred) so the cuts read as intentional.
  Punches only on stressed words: rejected, rejection, denied, red, now, That's it, 60.
- Voice is cut on the same segments as the picture; no music (none supplied).

## Layout notes (found in review)

- Her head sits lower after the hook, leaving only ~330px between chin and captions, so the SOP
  page lives in a **left column** (x 64–364, y 640–1040): clear of her face (x≈420–720), the
  right-edge Reels buttons, and the caption block. The "hundred times" copies slap into a pile in
  the same column instead of fanning across her.
- The hook's falling sheets fade as they drop so white paper never sits behind white captions.
- Multi-instance components must have the internal composition id and timeline key equal to the
  host id. A shared id (`sop` × 4) passed lint/check but silently blanked the plate video while
  any instance was on screen. `tools/sop.template.html` is therefore written out once per host by
  `tools/build.py` (`compositions/sop-*.html`).

## Palette additions

| Role | Hex | Use |
| --- | --- | --- |
| Pen red | `#C41E2A` | markup strokes on paper (weak SOP) |
| Pen green | `#1F8A4C` | tick on the strong SOP (lime is unreadable on white paper) |
| Navy | `#1C2442` | brand card bar, tag, name |

## Build

```bash
npx hyperframes remove-background prachi-full.mp4 -o /tmp/subject-full.webm --quality best
tools/make_plate.sh /tmp/subject-full.webm   # dimmed-room plate, red-flag cutout, end-hold frame
python tools/make_assets.py                  # props (needs pillow numpy scipy fonttools brotli)
python tools/build.py                        # index.html + compositions/captions.html
npm run check && npm run render
```

Author in source seconds: `tools/build.py` (captions, camera, SFX, prop windows) and the
`compositions/*` variables. Each prop window sits inside one segment, so its local times are
source offsets.

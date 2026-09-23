# DESIGN: full reel (`prachi-full.mp4`, 50.8s source → 47.7s edit)

Extends the approved 10s cut in `../reel/` (its DESIGN.md is the base spec: palette, caption
finish, "no AI slop" rules). The first 9.5s here are the same hook, frame for frame.

## Scene system (v2: "motion graphics take centre stage")

The user rejected the pasted-on paper props ("cheap overlay") and asked for scenes at the level
of the three they liked: past → future line, DM composer, "why" badges. Clean, flat UI driven by
the dialogue. Rule for every beat now:

- **Insert** (face stays sharp): the graphic sits at chest height under her chin.
- **Full scene**: the footage is replaced by a blurred copy of itself plus a vignette
  (`SCENE_BG` in `tools/build.py`, from `assets/media/blur-*.mp4`). The graphic sits in the
  centre, and when it carries the words itself, that caption group is dropped (`DROP` / `SUPPRESS`).
- One visual language: off-white `card-light` slabs, dark `glass-dark` bars, lime/red accents,
  Archivo, one light pass per surface, `expo.out` entrances, `back.out` only on small badges.

| Source s | Line | Scene | Type |
| --- | --- | --- | --- |
| 0–1.9 | "Your visa got rejected" | `visa-status`: status pill goes from pending dots to red REJECTED; red backdrop behind her | insert |
| 2.0–4.4 | "this one document is probably why" | `doc-pick`: five documents, four drop, one is lifted and ringed; red "?" on "why" | insert |
| 7.5–9.6 | "after the rejection letter arrives" | `letter`: notification drops in over the blurred B&W frame, buzzes on "arrives" | full |
| 9.56–12.5 | "It's called your statement of purpose" | `sop-title`: kinetic words, initials in lime, collapse into "SOP" + underline | full, no captions |
| 12.5–16.0 | "…getting it wrong… visas get denied" | captions, punch on "denied" | face |
| 16.6–21.8 | "A weak SOP has generic goals, copied lines, zero personal story" | `slabs-weak`: header with red WEAK SOP pill, three icon slabs stack per phrase, each gets a red ✕ | full, no captions |
| 22.2–24.6 | "The officer has seen it a hundred times" | `hundred`: one SOP, then 99 identical copies fill a 10×10 grid, ×1 → ×100 | full |
| 25.0–26.2 | "Instant red flag" | red backdrop behind her | face |
| 28.2–29.2 | "answers three things" | `slabs-strong`: three numbered empty slabs, answered next by the "why" badges | full |
| 29.7–32.6 | "Why this country / course / now" | numbered badge captions (kept, user favourite) | face |
| 33.4–37.2 | "connects your past to your future in one clean line" | `past-future` (kept) | insert |
| 39.0–40.9 | "in the next 60 days" | 60 counts up (kept) | face |
| 41.1–44.8 | "Work Abroad Consultancy… free SOP reviews this month" | `brand`: compact name card, then offer and month pills arrive as spoken | full, no captions |
| 45.5–48.0 | "DM the word SOP or hit the link in bio" | `dm` (kept) | insert |
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
| Red tint | `#FFE6E8` / `#D61F31` | icon tiles on the weak-SOP slabs |
| Navy | `#1C2442` | brand card bar, tag, name |

## Build

```bash
npx hyperframes remove-background prachi-full.mp4 -o /tmp/subject-full.webm --quality best
tools/make_plate.sh /tmp/subject-full.webm   # dimmed-room plate, red-flag cutout, end-hold frame, blur plates
python tools/build.py                        # index.html + every compositions/*.html from tools/scenes
npm run check && npm run render
```

Author in source seconds: `tools/build.py` (captions, camera, SFX, prop windows) and the
`compositions/*` variables. Each prop window sits inside one segment, so its local times are
source offsets.

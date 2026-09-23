---
workflow: general-video
flow: automation
storyboard: no
message: "Your visa may have been rejected because of one document — most students only find out after the letter arrives."
destination: instagram-reels
aspect: "9:16"
language: en
length: 10.12s
---

## Intent

Turn the supplied 10s talking-head clip into a polished short-form reel with an After
Effects-style finish: accurate word-timed captions, strong typography, natural zooms and
reframes, kinetic emphasis, tasteful paperwork-themed motion graphics, subtle sound-aware
details. Footage and dialogue are the source of truth — no invented claims or visuals.

## Assets

- `prachi-original-first-10s.mp4` — 1080×1920, 25fps, 10.12s, AAC stereo voice (no music).
- `transcript.json` — faster-whisper medium.en word timings; word w11 corrected to "Most"
  (large-v3 cross-check, p=0.92).
- `data/audio-data.json` — per-frame RMS + 8 bands at 25fps (voice envelope).
- `assets/fonts/` — Archivo upright + italic variable (OFL, Google Fonts).
- `assets/media/subject.webm` — `hyperframes remove-background` cutout (quality best).
- `assets/media/bw.mp4`, `assets/media/blur.mp4` — ffmpeg-preprocessed B&W and blur variants.
- Style references (user-supplied, not shipped): tubetactix, ManavSharma, 123faadkhan,
  luemmy21 reels.

## Customizations

- v1 "Case File" (cream editorial) was rejected by the user ("nah i dont like it").
- v2 design spec: `DESIGN.md` ("Creator Punch"), derived from the reference reels.

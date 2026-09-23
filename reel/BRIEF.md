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
- `assets/fonts/` — Archivo variable, Instrument Serif (OFL, Google Fonts).

## Customizations

- Design spec: `DESIGN.md` ("Case File").

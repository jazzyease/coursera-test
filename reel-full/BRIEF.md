---
workflow: general-video
flow: automation
storyboard: no
message: "Your visa may have been rejected because of your statement of purpose; here is what a weak vs strong SOP looks like, and how to get a free review."
destination: instagram-reels
aspect: "9:16"
language: en
length: 47.72s
---

## Intent

Full-length edit of `prachi1.2.mp4` (50.8s) in the style approved on the 10s cut (`../reel/`):
reference-style gradient captions, photoreal props, restrained motion, no AI-slop effects. The
user asked for "a good job, not an AI slop job".

## Assets

- `prachi-full.mp4`: source, 1080×1920, 25fps, 50.8s. First 10.12s are frame-identical to the
  10s clip.
- `transcript.json`: faster-whisper medium.en word timings, cross-checked with large-v3 (identical
  words). Fixes: "Dn" → "DM"; words 0–20 use the hand-validated 10s alignment; "and" (12.2s) and
  "A" (26.96s) snapped out of silence the model had absorbed.
- Brand name "Work Abroad Consultancy" is as spoken; spelling is unverified.

## Customizations

- Jump cuts on sentence pauses; end freeze 1.24s. See DESIGN.md.

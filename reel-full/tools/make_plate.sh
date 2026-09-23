#!/usr/bin/env bash
# Bake the footage treatment into one plate so every jump-cut segment references one source:
#   source -> room dimmed (radial, darker at the edges) -> subject cutout laid back on top at full
#   brightness. Also trims the cutout used for the "instant red flag" red backdrop.
#
# Needs: ffmpeg with libvpx-vp9, python3 + pillow/numpy, and the subject cutout from
#   npx hyperframes remove-background prachi-full.mp4 -o /tmp/subject-full.webm --quality best
set -euo pipefail
cd "$(dirname "$0")/.."
CUT="${1:-/tmp/subject-full.webm}"

python3 - <<'EOF'
# Same dim as the 10s cut's CSS: rgba(14,11,16,.12) under
# radial-gradient(ellipse 70% 55% at 52% 42%, rgba(14,11,16,.28), rgba(14,11,16,.62)).
import numpy as np
from PIL import Image
W, H = 1080, 1920
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.clip(np.hypot((xx - 0.52 * W) / (0.70 * W), (yy - 0.42 * H) / (0.55 * H)), 0, 1)
a_rad = 0.28 + (0.62 - 0.28) * r
a = 1 - (1 - 0.12) * (1 - a_rad)  # two stacked layers of the same colour
img = np.dstack([np.full((H, W), c, np.uint8) for c in (14, 11, 16)] + [(a * 255).astype(np.uint8)])
Image.fromarray(img, "RGBA").save("/tmp/dim.png")
EOF

ffmpeg -loglevel error -y -i prachi-full.mp4 -loop 1 -i /tmp/dim.png -c:v libvpx-vp9 -i "$CUT" \
  -filter_complex "[0:v][1:v]overlay=shortest=1[d];[d][2:v]overlay=eof_action=pass,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 -preset medium -g 25 -movflags +faststart assets/media/plate.mp4

ffmpeg -loglevel error -y -c:v libvpx-vp9 -i "$CUT" -ss 24.88 -t 1.48 \
  -c:v libvpx-vp9 -pix_fmt yuva420p -crf 18 -b:v 0 -auto-alt-ref 0 assets/media/cutout-redflag.webm
# Freeze frame for the end hold (last source frame, from the treated plate).
ffmpeg -loglevel error -y -sseof -0.08 -i assets/media/plate.mp4 -frames:v 1 -q:v 2 assets/media/end-hold.jpg
# Blurred plates for full scenes (colour, and B&W for the hook's black-and-white stretch).
ffmpeg -loglevel error -y -i assets/media/plate.mp4 -an -vf "scale=540:960,gblur=sigma=18,eq=brightness=-0.03:saturation=0.92" \
  -c:v libx264 -crf 20 -preset medium -g 25 -pix_fmt yuv420p assets/media/blur-full.mp4
ffmpeg -loglevel error -y -i assets/media/plate.mp4 -t 10.12 -an -vf "scale=540:960,gblur=sigma=18,hue=s=0,eq=brightness=-0.05:contrast=1.08" \
  -c:v libx264 -crf 20 -preset medium -g 25 -pix_fmt yuv420p assets/media/blur-bw.mp4
echo "plate, red-flag cutout, end-hold frame and blur plates written"

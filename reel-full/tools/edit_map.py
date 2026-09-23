"""Jump-cut edit map for prachi-full.mp4: the single source of truth for every cut.

Each CUT removes [start, end) of source time (all cuts sit in measured silence, 37–90 dB below
speech; see DESIGN.md). Everything else in the project is authored in *source* seconds and mapped
to output seconds with `out()`. Each prop sub-composition lives entirely inside one segment, so its
internal offsets equal source offsets.

    python tools/edit_map.py            -> prints segment <video>/<audio> HTML + output duration,
                                           writes data/transcript-output.json
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_END = 50.76
CUTS = [
    (16.08, 16.64),
    (21.80, 22.24),
    (24.60, 24.88),
    (26.36, 26.88),
    (29.24, 29.60),
    (32.76, 33.36),
    (38.20, 38.92),
    (44.76, 45.24),
    (48.16, 48.48),
]


def segments():
    segs, t = [], 0.0
    for a, b in CUTS:
        segs.append((t, a))
        t = b
    segs.append((t, SOURCE_END))
    return segs


def out(src):
    """Map a source time to output time. Times inside a cut snap to the cut point."""
    shift = 0.0
    for a, b in CUTS:
        if src >= b:
            shift += b - a
        elif src > a:
            return round(a - shift, 3)
    return round(src - shift, 3)


END_HOLD = 1.24  # freeze on the last frame so the closing line ("…cost you a year") can be read


def total():
    return round(out(SOURCE_END) + END_HOLD, 3)


def html():
    lines = []
    for i, (a, b) in enumerate(segments()):
        s, d = out(a), round(b - a, 3)
        lines.append(
            f'<video id="seg-{i}" class="clip" src="assets/media/plate.mp4" muted playsinline '
            f'data-start="{s}" data-media-start="{a}" data-duration="{d}" data-track-index="0"></video>'
        )
    for i, (a, b) in enumerate(segments()):
        s, d = out(a), round(b - a, 3)
        lines.append(
            f'<audio id="vo-{i}" src="prachi-full.mp4" data-start="{s}" data-media-start="{a}" '
            f'data-duration="{d}" data-track-index="10" data-volume="1"></audio>'
        )
    return "\n".join(lines)


if __name__ == "__main__":
    print(html())
    print("segments", segments())
    print("output duration", total())
    src = json.load(open(os.path.join(ROOT, "transcript.json")))
    mapped = [dict(w, start=out(w["start"]), end=out(w["end"])) for w in src]
    json.dump(mapped, open(os.path.join(ROOT, "data", "transcript-output.json"), "w"), indent=1)

"""Generate index.html and compositions/captions.html from the templates in tools/.

Everything here is authored in SOURCE seconds (the raw clip) and mapped through the jump cuts in
tools/edit_map.py, so the edit can be re-cut by changing CUTS and re-running:
    python tools/build.py
"""

import json
import os

from edit_map import CUTS, END_HOLD, SOURCE_END, html as seg_html, out, segments, total

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORDS = json.load(open(os.path.join(ROOT, "transcript.json")))
W = [[w["start"], w["text"].rstrip(",")] for w in WORDS]


def ws(i):
    return WORDS[i]["start"]


# --------------------------------------------------------------------------- captions
# (first word, last word) index ranges map to the transcript; groups hard-swap at the next start.
def G(l1, l2, tone, size, **kw):
    first = (l1 or l2[0])[0]
    return dict(l1=l1, l2=l2, tone=tone, size=size, start=ws(first), **kw)


GROUPS = [
    # hook (identical to the approved 10s cut)
    G([0, 1, 2], [[3]], "red", 140, hero=[3], start0=0.0),
    G([4, 5], [[6, 7]], "lime", 84, badge=dict(before=6, text="1")),
    G([8, 9], [[10]], "lime", 156, hero=[10]),
    G([11, 12], [[13, 14, 15]], "lime", 88),
    G([16, 17], [[18], [19]], "red", 124),
    G([], [[20]], "white", 156, hero=[20]),
    # the term
    G([21, 22, 23], [[24], [25, 26]], "lime", 104),
    G([27, 28], [[29, 30]], "red", 124),
    G([31, 32, 33], [[34, 35]], "white", 96),
    G([36, 37], [[38]], "red", 150, hero=[38]),
    # weak SOP
    G([39], [[40, 41]], "red", 130),
    G([42], [[43], [44]], "white", 116),
    G([], [[45], [46]], "white", 124),
    G([47], [[48], [49]], "red", 116),
    G([50, 51], [[52, 53, 54]], "white", 100),
    G([55], [[56], [57]], "lime", 120),
    G([58], [[59, 60]], "red", 140, hero=[59, 60]),
    # strong SOP
    G([61], [[62], [63]], "lime", 130),
    G([64], [[65], [66]], "lime", 120),
    G([], [[67, 68], [69]], "white", 110, badge=dict(before=67, text="1")),
    G([], [[70, 71], [72]], "white", 110, badge=dict(before=70, text="2")),
    G([], [[73], [74]], "lime", 150, badge=dict(before=73, text="3"), hero=[74]),
    # past -> future
    G([75, 76], [[77, 78]], "white", 110),
    G([79], [[80, 81]], "lime", 104),
    G([82, 83], [[84, 85]], "lime", 108),
    G([], [[86, 87]], "white", 124, hero=[86, 87]),
    # offer
    G([88, 89], [[90]], "white", 120),
    G([91, 92, 93], [[94, 95]], "lime", 150, hero=[94], count=True),
    G([], [[96, 97], [98]], "white", 96),
    G([99, 100], [[101, 102], [103]], "lime", 110),
    G([], [[104, 105]], "white", 104),
    # CTA
    G([106, 107, 108], [[109]], "lime", 156, hero=[109]),
    G([110, 111, 112], [[113, 114, 115]], "white", 100),
    # close
    G([116, 117, 118], [[119], [120]], "white", 116),
    G([], [[121, 122], [123, 124]], "red", 132, hero=[124]),
]
for i, g in enumerate(GROUPS):
    if "start0" in g:
        g["start"] = g.pop("start0")
    nxt = GROUPS[i + 1]["start"] if i + 1 < len(GROUPS) else 99
    g["end"] = nxt
GROUPS[-1]["end"] = 60  # holds through the end freeze
# hold through the hook's blur pause (source 4.44-5.12) exactly as in the 10s cut
GROUPS[2]["end"] = 4.44

# --------------------------------------------------------------------------- camera / colour (JS)
MOMENTS = """
        // ---------- Colour moments ----------
        tl.set("#red-hook", { opacity: 1 }, o(0.94));             // "rejected"
        tl.to("#red-hook", { opacity: 0, duration: 0.3, ease: "power2.in" }, o(1.6));
        tl.set("#flash", { opacity: 0.4 }, o(7.54));              // "rejection" -> black and white
        tl.to("#flash", { opacity: 0, duration: 0.16, ease: "power2.out" }, o(7.58));
        tl.set("#bw-wrap", { opacity: 1 }, o(7.54));
        tl.set("#bw-wrap", { opacity: 0 }, o(9.56));              // colour returns on "It's called…"
        tl.set("#flash", { opacity: 0.3 }, o(9.56));
        tl.to("#flash", { opacity: 0, duration: 0.2, ease: "power2.out" }, o(9.6));
        tl.to("#blur-wrap", { opacity: 1, duration: 0.16, ease: "power2.in" }, o(4.4));
        tl.to("#blur-wrap", { opacity: 0, duration: 0.06, ease: "none" }, o(5.08));
        tl.set("#red-flag", { opacity: 1 }, o(25.46));            // "instant RED flag"
        tl.to("#red-flag", { opacity: 0, duration: 0.3, ease: "power2.in" }, o(26.06));

        // ---------- Camera: alternate framing on every jump cut, punch only on stressed words ----------
        cam({ scale: 1.16, x: 0, y: 0 }, 0);
        cam({ scale: 1.04 }, 0, 0.45, "power3.out");
        cam({ scale: 1.08 }, 0.45, 0.45);
        cam({ scale: 1.16 }, 0.92, 0.14, "power3.out");   // "rejected"
        shake(0.96, 5);
        cam({ scale: 1.24 }, 1.05, 0.9);
        cam({ scale: 1.0 }, 1.96);
        cam({ scale: 1.08 }, 1.96, 2.44);
        cam({ scale: 1.2 }, 4.4, 0.7, "power2.in");       // push through the blur
        cam({ scale: 1.14 }, 5.12);
        cam({ scale: 1.18 }, 5.12, 1.72);
        cam({ scale: 1.02 }, 6.84);
        cam({ scale: 1.05 }, 6.84, 0.7);
        cam({ scale: 1.16 }, 7.54, 0.14, "power3.out");   // "rejection"
        cam({ scale: 1.22 }, 7.7, 0.58);
        cam({ scale: 1.06 }, 8.28);
        cam({ scale: 1.1 }, 8.28, 1.28);
        shake(9.05, 4);                                   // stamp lands
        cam({ scale: 1.03 }, 9.56);                       // colour back, room for the SOP page
        cam({ scale: 1.07 }, 9.56, 2.76);
        cam({ scale: 1.1 }, 12.34);                       // "getting it wrong"
        cam({ scale: 1.12 }, 12.34, 3.1);
        cam({ scale: 1.2 }, 15.5, 0.14, "power3.out");    // "denied"
        shake(15.54, 4);
        cam({ scale: 1.03 }, 16.64);                      // cut: weak SOP
        cam({ scale: 1.07 }, 16.64, 5.1);
        cam({ scale: 1.06 }, 22.24);                      // cut: officer
        cam({ scale: 1.09 }, 22.24, 2.3);
        cam({ scale: 1.12 }, 24.88);                      // cut: instant red flag
        cam({ scale: 1.2 }, 25.46, 0.14, "power3.out");
        shake(25.5, 4);
        cam({ scale: 1.03 }, 26.88);                      // cut: strong SOP
        cam({ scale: 1.06 }, 26.88, 2.3);
        cam({ scale: 1.08 }, 29.6);                       // cut: why this country
        cam({ scale: 1.14 }, 31.0);                       // why this course
        cam({ scale: 1.22 }, 32.12);                      // why now
        cam({ scale: 1.02 }, 33.36);                      // cut: past -> future
        cam({ scale: 1.06 }, 33.36, 4.1);
        cam({ scale: 1.13 }, 37.52, 0.16, "power3.out");  // "That's it."
        cam({ scale: 1.08 }, 38.92);                      // cut: offer
        cam({ scale: 1.11 }, 38.92, 1.1);
        cam({ scale: 1.17 }, 40.08, 0.14, "power3.out");  // "60"
        cam({ scale: 1.03 }, 41.1);                       // room for the brand card
        cam({ scale: 1.06 }, 41.1, 3.6);
        cam({ scale: 1.02 }, 45.24);                      // cut: DM
        cam({ scale: 1.05 }, 45.24, 2.9);
        cam({ scale: 1.1 }, 48.48);                       // cut: close, slow push in
        cam({ scale: 1.26 }, 48.48, 2.28 + 1.24, "sine.inOut");  // continues through the end freeze"""

# --------------------------------------------------------------------------- prop hosts
# (id, composition, source start, source end, variables). Each window sits inside one segment,
# so the variables' local times are simply (source time - source start).
HOSTS = [
    ("passport", "passport.html", 0.0, 1.98, None),
    ("doc-stack", "doc-stack.html", 1.96, 4.56, None),
    ("envelope", "envelope.html", 8.02, 9.62, None),
    ("sop-intro", "sop-intro.html", 9.5, 14.6, dict(mode="intro", inAt=0.06, outAt=4.86, dur=5.1)),
    ("sop-weak", "sop-weak.html", 16.64, 21.8, dict(mode="weak", inAt=0.18, a=17.98 - 16.64, b=19.22 - 16.64, c=20.48 - 16.64, dur=5.16)),
    ("sop-copies", "sop-copies.html", 22.24, 24.6, dict(mode="copies", a=23.5 - 22.24, outAt=2.1, dur=2.36)),
    ("sop-strong", "sop-strong.html", 26.88, 29.24, dict(mode="strong", inAt=0.06, a=0.52, outAt=2.1, dur=2.36)),
    ("past-future", "past-future.html", 33.36, 37.66, dict(pastAt=0.8, futureAt=1.6, lineAt=2.42, outAt=4.04, dur=4.3)),
    ("brand", "brand.html", 41.1, 44.76, dict(offerAt=42.84 - 41.1, outAt=3.4)),
    ("dm", "dm.html", 45.24, 48.16, dict(typeAt=45.72 - 45.24, sendAt=46.3 - 45.24, linkAt=47.3 - 45.24, outAt=2.66)),
]

# --------------------------------------------------------------------------- SFX (source s)
SFX = [
    ("pp-in", "whoosh-short", 0.02, 0.3), ("rejected", "impact-bass-1", 0.94, 0.32),
    ("fan", "whoosh", 1.96, 0.26), ("badge1", "pop", 2.3, 0.3), ("doc", "whoosh-short", 2.3, 0.34),
    ("why", "click", 4.02, 0.4), ("blur", "whoosh", 4.36, 0.3), ("cut", "click", 5.12, 0.3),
    ("bw", "impact-bass-1", 7.52, 0.2), ("letter", "whoosh-short", 8.04, 0.34), ("flap", "click-soft", 8.44, 0.5),
    ("stamp", "impact-bass-1", 9.02, 0.36), ("sop-in", "whoosh-short", 9.54, 0.26),
    ("denied", "impact-bass-1", 15.5, 0.2), ("weak-in", "whoosh-short", 16.8, 0.22),
    ("mark1", "click-soft", 17.98, 0.4), ("mark2", "click-soft", 19.22, 0.4), ("mark3", "click-soft", 20.48, 0.4),
    ("copies", "whoosh", 23.48, 0.24), ("redflag", "impact-bass-1", 25.44, 0.26),
    ("strong-in", "whoosh-short", 26.92, 0.22), ("tick", "pop", 27.4, 0.2),
    ("b1", "pop", 29.7, 0.22), ("b2", "pop", 30.98, 0.22), ("b3", "pop", 32.1, 0.22),
    ("node1", "click-soft", 34.16, 0.4), ("node2", "click-soft", 34.96, 0.4), ("line", "whoosh-short", 35.78, 0.18),
    ("sixty", "click", 40.08, 0.26), ("brand-in", "whoosh-short", 41.1, 0.24),
    ("type", "key-press", 45.72, 0.3), ("send", "pop", 46.3, 0.26), ("link", "click-soft", 47.3, 0.45),
]
SFX_DUR = {"whoosh-short": 0.57, "whoosh": 0.57, "impact-bass-1": 1.0, "pop": 0.7, "click": 0.36, "click-soft": 0.36, "key-press": 0.4}


def attrs(d):
    return json.dumps(d, separators=(",", ":")).replace("'", "&#39;")


def main():
    T = open(os.path.join(ROOT, "tools", "index.template.html")).read()
    seg = seg_html().split("\n")
    videos = "\n".join("          " + l for l in seg if l.startswith("<video"))
    # Voice segments alternate between two tracks so abutting windows never share one.
    voice = "\n".join(
        "      " + l.replace('data-track-index="10"', f'data-track-index="{10 + k % 2}"')
        for k, l in enumerate(x for x in seg if x.startswith("<audio"))
    )
    hosts = []
    for hid, comp, s, e, var in HOSTS:
        v = f" data-variable-values='{attrs(var)}'" if var else ""
        hosts.append(
            f'      <div id="{hid}-slot" style="position: absolute; inset: 0">\n'
            f'        <div id="{hid}" data-composition-id="{hid}" data-composition-src="compositions/{comp}"{v} '
            f'data-start="{out(s)}" data-duration="{round(e - s, 3)}" data-track-index="4" data-width="1080" data-height="1920"></div>\n'
            f"      </div>"
        )
    sfx = []
    for sid, f, s, vol in SFX:
        sfx.append(
            f'      <audio id="sfx-{sid}" src="assets/sfx/{f}.mp3" data-start="{out(s)}" data-duration="{SFX_DUR[f]}" '
            f'data-track-index="{12 + len(sfx) % 5}" data-volume="{vol}"></audio>'
        )
    rep = {
        "{{TOTAL}}": str(total()),
        "{{SEGMENTS}}": videos,
        "{{VOICE}}": voice,
        "{{SFX}}": "\n".join(sfx),
        "{{HOSTS}}": "\n".join(hosts),
        "{{HOLD_START}}": str(out(SOURCE_END)),
        "{{HOLD_DUR}}": str(END_HOLD),
        "{{REDFLAG_START}}": str(out(24.88)),
        "{{REDFLAG_DUR}}": "1.48",
        "{{CUTS}}": json.dumps(CUTS),
        "{{WORDS}}": json.dumps(W),
        "{{GROUPS}}": json.dumps(GROUPS),
        "{{MOMENTS}}": MOMENTS,
    }
    for k, v in rep.items():
        T = T.replace(k, v)
    assert "{{" not in T, "unfilled placeholder in index template"
    open(os.path.join(ROOT, "index.html"), "w").write(T)
    C = open(os.path.join(ROOT, "tools", "captions.template.html")).read()
    for k in ("{{CUTS}}", "{{WORDS}}", "{{GROUPS}}"):
        assert k in C, k
        C = C.replace(k, rep[k])
    open(os.path.join(ROOT, "compositions", "captions.html"), "w").write(C)
    # Multi-instance component: one file per host, ids matched to the host.
    S = open(os.path.join(ROOT, "tools", "sop.template.html")).read()
    for hid, comp, *_ in HOSTS:
        if comp.startswith("sop-"):
            open(os.path.join(ROOT, "compositions", comp), "w").write(S.replace("__ID__", hid))
    print("index.html written; duration", total(), "segments", len(segments()), "groups", len(GROUPS))


if __name__ == "__main__":
    main()

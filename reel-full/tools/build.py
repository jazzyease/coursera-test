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
for g in GROUPS:
    if "start0" in g:
        g["start"] = g.pop("start0")
for g in GROUPS:
    # v3: reference-scale type (luemmy21): accents ~80% of v2, heroes capped.
    g["size"] = min(round(g["size"] * 0.8), 128)

# Scenes that carry their own words replace these caption groups:
#   6 "It's called your statement of purpose" -> sop-title
#   10-13 "A weak SOP has generic goals, copied lines, zero personal story" -> slabs-weak
#   28-30 "Work Abroad Consultancy is doing free SOP reviews this month" -> brand
#   14-15 "The officer has seen it a hundred times" -> hundred
#   27 "in the next 60 days" -> ring-60
DROP = {6, 10, 11, 12, 13, 14, 15, 27, 28, 29, 30}
SUPPRESS = [(9.56, 12.5), (16.64, 21.8), (22.24, 24.6), (39.66, 41.1), (41.1, 44.76)]  # source windows with no captions
GROUPS = [g for i, g in enumerate(GROUPS) if i not in DROP]
for g in GROUPS:
    for a, b in SUPPRESS:
        if a <= g["start"] < b:
            g["start"] = b
for i, g in enumerate(GROUPS):
    nxt = GROUPS[i + 1]["start"] if i + 1 < len(GROUPS) else 60  # last group holds through the end freeze
    g["end"] = min([nxt] + [a for a, _ in SUPPRESS if a > g["start"]])
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
def L(src, start):
    """Local time inside a host that starts at source `start` (correct across jump cuts)."""
    return round(out(src) - out(start), 3)


def w(i):
    return WORDS[i]["start"]


HOSTS = [
    # (host id, template or fixed composition, source start, source end, CFG in LOCAL seconds)
    ("visa-status", "scenes/visa-status.html", 0.0, 1.98, dict(inAt=0.04, flip=0.94, outAt=1.74)),
    ("doc-pick", "scenes/doc-pick.html", 1.96, 4.5, dict(inAt=0.1, pick=0.3, ring=0.46, why=2.08, outAt=2.36)),
    ("letter", "scenes/letter.html", 8.02, 9.56, dict(inAt=0.02, land=0.3, outAt=1.3)),
    # Runs past the caption resume (12.5): the SOP card sits at the chest, captions below it.
    ("sop-title", "scenes/sop-title.html", 9.5, 13.1, dict(inAt=0.04, l0=[0.06, 0.72, 0.98], words=[1.16, 1.58, 1.82], collapse=2.2, outAt=3.36)),
    ("slabs-weak", "scenes/slabs.html", 16.64, 21.8, dict(
        top=736, h=132, gap=14, outAt=None,
        tab=dict(text="WEAK SOP", tone="red", at=L(w(40), 16.64) - 0.04),
        slabs=[dict(text="Generic goals", at=L(w(43), 16.64) - 0.06, x=L(18.94, 16.64), slot="icon-goals", tone="red"),
               dict(text="Copied lines", at=L(w(45), 16.64) - 0.06, x=L(20.06, 16.64), slot="icon-copy", tone="red"),
               dict(text="Zero personal story", at=L(w(47), 16.64) - 0.06, x=L(21.62, 16.64) - 0.08, slot="icon-story", tone="red")])),
    ("hundred", "scenes/hundred.html", 22.24, 24.6, dict(
        inAt=0.02, h0=[max(0.04, L(w(i), 22.24) - 0.04) for i in range(50, 55)],
        h1=[L(w(i), 22.24) - 0.04 for i in (55, 56, 57)], fill=L(w(56), 22.24) - 0.1)),
    ("tiles-why", "scenes/tiles-why.html", 26.88, 32.76, dict(
        pop=[L(w(65), 26.88) - 0.06, L(w(65), 26.88) + 0.08, L(w(66), 26.88)],
        flip=[L(w(67), 26.88) - 0.04, L(w(70), 26.88) - 0.04, L(w(73), 26.88) - 0.04], outAt=L(32.76, 26.88) - 0.2)),
    ("past-future", "past-future.html", 33.36, 37.66, dict(pastAt=0.8, futureAt=1.6, lineAt=2.42, outAt=4.04, dur=4.3)),
    ("ring-60", "scenes/ring-60.html", 39.66, 41.1, dict(
        lead=[max(0.06, L(w(i), 39.66) - 0.02) for i in (91, 92, 93)], inAt=0.0, count=L(w(94), 39.66) - 0.06, outAt=1.26)),
    ("brand", "scenes/slabs.html", 41.1, 44.76, dict(
        top=736, h=132, gap=14, outAt=None, tab=None,
        slabs=[dict(text="Work Abroad Consultancy", big=True, at=L(w(96), 41.1) - 0.08),
               dict(text="Free SOP reviews", at=L(w(101), 41.1) - 0.06, slot="icon-review", tone="lemon"),
               dict(text="This month", at=L(w(104), 41.1) - 0.06, slot="icon-calendar", tone="navy")])),
    ("dm", "dm.html", 45.24, 48.16, dict(typeAt=45.72 - 45.24, sendAt=46.3 - 45.24, linkAt=47.3 - 45.24, outAt=2.66)),
]

# v3: no blurred-footage scenes. Light cutaways (sop-title, hundred) draw their own ground.
SCENE_BG = []

# --------------------------------------------------------------------------- SFX (source s)
SFX = [
    ("vs-in", "whoosh-short", 0.04, 0.26), ("rejected", "impact-bass-1", 0.9, 0.3),
    ("tiles", "whoosh", 2.06, 0.2), ("badge1", "pop", 2.26, 0.26), ("pick", "click-soft", 2.42, 0.45),
    ("why", "pop", 4.04, 0.26), ("blur", "whoosh", 4.36, 0.3), ("cut", "click", 5.12, 0.3),
    ("bw", "impact-bass-1", 7.52, 0.2), ("notif", "whoosh-short", 8.04, 0.3), ("buzz", "click", 8.32, 0.34),
    ("sop-c1", "pop", 10.62, 0.2), ("sop-c2", "pop", 11.04, 0.18), ("sop-c3", "pop", 11.28, 0.2),
    ("sop-fly", "whoosh", 11.74, 0.24), ("sop-land", "click-soft", 12.26, 0.45),
    ("denied", "impact-bass-1", 15.5, 0.2),
    ("weak-tab", "pop", 16.86, 0.22),
    ("slab1", "whoosh-short", 17.92, 0.2), ("x1", "click", 19.06, 0.32),
    ("slab2", "whoosh-short", 19.16, 0.2), ("x2", "click", 20.18, 0.32),
    ("slab3", "whoosh-short", 20.42, 0.2), ("x3", "click", 21.66, 0.32),
    ("hundred-in", "whoosh-short", 22.24, 0.24), ("fill", "whoosh", 23.46, 0.26), ("count", "pop", 24.0, 0.2),
    ("redflag", "impact-bass-1", 25.44, 0.26),
    ("t1", "pop", 28.32, 0.2), ("t2", "pop", 28.46, 0.2), ("t3", "pop", 28.72, 0.2),
    ("f1", "whoosh-short", 29.7, 0.22), ("f2", "whoosh-short", 30.98, 0.22), ("f3", "whoosh-short", 32.1, 0.22),
    ("node1", "click-soft", 34.16, 0.4), ("node2", "click-soft", 34.96, 0.4), ("line", "whoosh-short", 35.78, 0.18),
    ("ring", "whoosh-short", 39.96, 0.2), ("sixty", "click", 40.08, 0.26),
    ("brand-in", "whoosh-short", 41.12, 0.24), ("offer", "pop", 42.78, 0.22), ("month", "pop", 43.92, 0.2),
    ("type", "key-press", 45.72, 0.3), ("send", "pop", 46.3, 0.26), ("link", "click-soft", 47.3, 0.45),
]
SFX_DUR = {"whoosh-short": 0.57, "whoosh": 0.57, "impact-bass-1": 1.0, "pop": 0.7, "click": 0.36, "click-soft": 0.36, "key-press": 0.4}


def attrs(d):
    return json.dumps(d, separators=(",", ":")).replace("'", "&#39;")


# --------------------------------------------------------------------------- scene templates
# Built-in line icons for every custom-asset slot (ASSET_PROMPTS.md). A file at
# assets/custom/<name>.png replaces the icon on the next build.
_SV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{}</svg>'
ICONS = {
    "passport": _SV.format('<rect x="5" y="2.5" width="14" height="19" rx="2.2"/><circle cx="12" cy="10.5" r="3.6"/><path d="M8.4 10.5h7.2M12 6.9c1.3 1 1.3 6.2 0 7.2M12 6.9c-1.3 1-1.3 6.2 0 7.2M9 17.5h6"/>'),
    "envelope": _SV.format('<rect x="2.5" y="5" width="19" height="14" rx="2.4"/><path d="M3.2 6.4l8.8 6.6 8.8-6.6"/>'),
    "icon-goals": _SV.format('<circle cx="11" cy="13" r="8"/><circle cx="11" cy="13" r="4.4"/><circle cx="11" cy="13" r="1.2"/><path d="M15.5 8.5L20 4M17 4h3v3"/>'),
    "icon-copy": _SV.format('<rect x="8" y="8" width="12.5" height="12.5" rx="2.2"/><path d="M16 8V5.5A2 2 0 0 0 14 3.5H5.5a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2H8"/>'),
    "icon-story": _SV.format('<circle cx="9" cy="8" r="3.4"/><path d="M3 20c.6-3.6 3-5.6 6-5.6s5.4 2 6 5.6"/><path d="M15.5 3.5h5a1 1 0 0 1 1 1v3.5a1 1 0 0 1-1 1h-2.3L16.5 11V9h-1a1 1 0 0 1-1-1V4.5a1 1 0 0 1 1-1z" stroke-dasharray="2 1.6"/>'),
    "icon-review": _SV.format('<path d="M6 3h8l4 4v6"/><path d="M6 3a1 1 0 0 0-1 1v15a1 1 0 0 0 1 1h5"/><circle cx="16.5" cy="16.5" r="3.6"/><path d="M19.2 19.2l2.3 2.3M15 16.6l1.1 1.1 2-2.2"/>'),
    "document": _SV.format('<path d="M6 2.5h8.5L19 7v14.5H6z"/><path d="M14.5 2.5V7H19"/><path d="M9 11.5h7M9 14.5h7M9 17.5h4.5"/>'),
    "icon-country": _SV.format('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 2.6 15.4 0 18M12 3c-2.6 2.6-2.6 15.4 0 18"/>'),
    "icon-course": _SV.format('<path d="M2.5 9.5L12 5l9.5 4.5L12 14z"/><path d="M6.5 11.6V16c0 1.5 2.5 3 5.5 3s5.5-1.5 5.5-3v-4.4"/><path d="M21.5 9.5v5"/>'),
    "icon-now": _SV.format('<circle cx="12" cy="13" r="8"/><path d="M12 9v4.4l3 1.8M9.5 2.5h5"/>'),
    "icon-calendar": _SV.format('<rect x="3.5" y="5" width="17" height="15.5" rx="2.4"/><path d="M3.5 10h17M8 3v4M16 3v4"/>'),
}
DOC_FALLBACK = ""  # the tile's CSS draws the document when no custom image is supplied


def custom(name):
    rel = f"assets/custom/{name}.png"
    return rel if os.path.exists(os.path.join(ROOT, rel)) else ""


def slot_html(name):
    src = custom(name)
    return f'<img class="slot-img" src="{src}" alt="" />' if src else ICONS[name]


def render_scene(hid, tpl, cfg):
    base = open(os.path.join(ROOT, "tools", "scenes", "_base.css")).read().rstrip("\n")
    S = open(os.path.join(ROOT, "tools", tpl)).read()
    if "slabs" in tpl:
        for sl in cfg["slabs"]:
            if "slot" in sl:
                sl["icon"], sl["hasImg"] = slot_html(sl["slot"]), "has-img" if custom(sl["slot"]) else ""
    doc = custom("document")
    logo = custom("logo")
    rep = {
        "__ID__": hid,
        "{{BASE_CSS}}": base,
        "{{CFG}}": json.dumps(cfg),
        "{{DOC}}": f'<img class="slot-img" src="{doc}" alt="" />' if doc else DOC_FALLBACK,
        "{{DOCCLS}}": "" if doc else "card-light",
        "{{DOCJS}}": json.dumps(f'<img class="slot-img" src="{doc}" alt="" />' if doc else ""),
        "{{LOGO}}": f'<div class="logo"><img src="{logo}" alt="" /></div>' if logo else "",
    }
    for name in ICONS:
        rep["{{SLOT:%s}}" % name] = slot_html(name)
        rep["{{HAS:%s}}" % name] = "has-img" if custom(name) else ""
    for k, v in rep.items():
        S = S.replace(k, v)
    assert "{{" not in S, (tpl, S[S.index("{{"):S.index("{{") + 40])
    open(os.path.join(ROOT, "compositions", hid + ".html"), "w").write(S)


def scene_bg_html():
    out_ = []
    for hid, src, s, e in SCENE_BG:
        out_.append(
            f'      <div class="sbg" id="sbg-{hid}">\n'
            f'        <video id="sbv-{hid}" class="clip" src="assets/media/{src}.mp4" muted playsinline data-start="{out(s)}" '
            f'data-media-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="5"></video>\n'
            f'        <div class="sdim"></div>\n      </div>'
        )
    return "\n".join(out_)


def scene_bg_moments():
    lines = ["        // ---------- Full scenes: blurred footage behind the graphic ----------"]
    starts = {round(s, 2) for _, _, s, _ in SCENE_BG}
    ends = {round(e, 2) for _, _, _, e in SCENE_BG}
    for hid, _, s, e in SCENE_BG:
        fin = 0.01 if round(s, 2) in ends else 0.16  # back-to-back scenes swap without a dip
        lines.append(f'        tl.to("#sbg-{hid}", {{ opacity: 1, duration: {fin}, ease: "power2.out" }}, o({s}));')
        if round(e, 2) not in starts:
            lines.append(f'        tl.to("#sbg-{hid}", {{ opacity: 0, duration: 0.12, ease: "power2.in" }}, o({e}) - 0.12);')
    return "\n".join(lines)


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
        if comp.startswith("scenes/"):
            render_scene(hid, comp, var)
            comp, var = hid + ".html", None
        v = f" data-variable-values='{attrs(var)}'" if var else ""
        hosts.append(
            f'      <div id="{hid}-slot" style="position: absolute; inset: 0">\n'
            f'        <div id="{hid}" data-composition-id="{hid}" data-composition-src="compositions/{comp}"{v} '
            f'data-start="{out(s)}" data-duration="{round(out(e) - out(s), 3)}" data-track-index="4" data-width="1080" data-height="1920"></div>\n'
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
        "{{MOMENTS}}": MOMENTS + "\n" + scene_bg_moments(),
        "{{SCENE_BG}}": scene_bg_html(),
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
    print("index.html written; duration", total(), "segments", len(segments()), "groups", len(GROUPS))


if __name__ == "__main__":
    main()

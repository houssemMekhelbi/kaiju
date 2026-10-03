#!/usr/bin/env python3
"""Generate the Kaiju icon theme next to this file (folders are Ember
plates with a Magma edge; documents are Ash outlines).

scalable/  64-unit SVGs. Folders are two terraced Ember plates (the 12/6 step
           cut top-left and bottom-right) with a cold edge that runs from ash to
           stone, and one Ash mark for the special folders. Documents are Raised
           Slag sheets in an Ash outline with the same terrace and one mark for
           their type (Blaze only on PDF, Spine on images and code). Devices are
           Slag boxes in the same cold line with a Magma light. The trash is a
           Magma-line bin.
16/        sidebar size: plain line icons in Ochre.
Anything not drawn here falls through to Adwaita.
Run: python3 build.py   (then gtk-update-icon-cache runs by itself)
"""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAME = "Kaiju"

GROUND, SLAG, RAISED, HAIR = "#0C0B0A", "#161311", "#221C18", "#3A2E26"
EMBER, EMBER_DEEP, MAGMA, ASH = "#9E3B14", "#5C2410", "#FF8A3D", "#ECE6DA"
SPINE, BLAZE = "#5FB8FF", "#FF3B3B"
SIDE = "#A89070"

GRAD = (f'<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#CFC6B4"/>'
        f'<stop offset="1" stop-color="#5A4E44"/></linearGradient>')   # accent choice E: ash to stone edges


def svg64(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">'
            f'<defs>{GRAD}</defs>{body}</svg>\n')


def write(rel, content, names):
    for name in names:
        path = ROOT / rel / f"{name}.svg"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


def stroke(d, color=ASH, w=2.4):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="square" stroke-linejoin="miter"/>'


# ---- folders: terraced plates --------------------------------------------------------
MARKS = {
    None: f'<polygon points="32,31 42,50 22,50" fill="{GROUND}" opacity="0.55"/>',
    "home": f'<path d="M23 50 V40 L32 31 L41 40 V50 Z" fill="{ASH}"/>',
    "documents": "".join(f'<rect x="22" y="{y}" width="{w}" height="2.6" fill="{ASH}"/>' for y, w in ((33, 20), (39.5, 20), (46, 13))),
    "downloads": stroke("M32 31 V46 M26 40.5 L32 46.5 L38 40.5 M24 51 H40"),
    "music": stroke("M28 48 V33 L39 31 V46") + f'<rect x="23" y="45.5" width="5.6" height="5" fill="{ASH}"/><rect x="34" y="43.5" width="5.6" height="5" fill="{ASH}"/>',
    "pictures": f'<path d="M21 51 L29 39 L33.5 45 L37 41 L44 51 Z" fill="{ASH}"/><polygon points="40,31 43.5,37 36.5,37" fill="{ASH}"/>',
    "videos": f'<path d="M27 32 L42 41 L27 50 Z" fill="{ASH}"/>',
    "desktop": stroke("M22 33 H42 V46 H22 Z M27 51 H37", ASH, 2.2),
    "templates": f'<rect x="23" y="32" width="18" height="18" fill="none" stroke="{ASH}" stroke-width="2.2" stroke-dasharray="3.4 2.8"/>',
    "share": stroke("M26 41.5 L38 35 M26 41.5 L38 48.5", ASH, 1.8) + "".join(f'<polygon points="{x},{y - 3.6} {x + 3.4},{y + 2.6} {x - 3.4},{y + 2.6}" fill="{ASH}"/>' for x, y in ((26, 41.5), (38, 34.5), (38, 48.5))),
    "remote": stroke("M32 32 a9 9.5 0 1 0 0.01 0 M23 41.5 H41 M32 32 C27 36.5 27 46.5 32 51 M32 32 C37 36.5 37 46.5 32 51", ASH, 1.7),
}


def folder(kind=None):
    body = (f'<path d="M4.75 16 H9 V11 H14 V6.75 H30 L35 14 H59.25 V56 H4.75 Z" fill="{EMBER_DEEP}" stroke="url(#edge)" stroke-width="1.5"/>'
            f'<path d="M4.75 30 H9 V25 H14 V20.75 H59.25 V50 H55 V55 H50 V59.25 H4.75 Z" fill="{EMBER}" stroke="url(#edge)" stroke-width="1.5"/>'
            + MARKS[kind])
    return svg64(body)


FOLDERS = {
    None: ["folder", "inode-directory", "folder-open", "folder-drag-accept", "folder-visiting"],
    "home": ["user-home", "folder-home"],
    "documents": ["folder-documents"],
    "downloads": ["folder-download"],
    "music": ["folder-music"],
    "pictures": ["folder-pictures"],
    "videos": ["folder-videos"],
    "templates": ["folder-templates"],
    "share": ["folder-publicshare"],
    "desktop": ["user-desktop"],
    "remote": ["folder-remote", "network-workgroup"],
}
for kind, names in FOLDERS.items():
    write("scalable/places", folder(kind), names)
    if kind is None:
        write("scalable/mimetypes", folder(kind), names)


# ---- documents: Ash outlines -----------------------------------------------------------
def sheet():
    return (f'<path d="M11.75 15 H16 V9 H22 V4.75 H52.25 V49 H48 V55 H42 V59.25 H11.75 Z" fill="{RAISED}" '
            f'stroke="{ASH}" stroke-opacity="0.8" stroke-width="1.5"/>')


def lines(ys, color=ASH, x0=19, x1=45, op=0.62):
    return "".join(f'<rect x="{x0}" y="{y}" width="{(x1 - x0) - (9 if i == len(ys) - 1 else 0)}" height="2" fill="{color}" opacity="{op}"/>'
                   for i, y in enumerate(ys))


DOC_MARKS = {
    None: "",
    "text": lines([23, 30, 37, 44]),
    "script": stroke("M20 25 L27 31 L20 37", SPINE) + stroke("M30 38 H43", SPINE) + lines([45, 51], ASH, 19, 40, 0.4),
    "code": stroke("M28 24 L21 33 L28 42", SPINE) + stroke("M37 24 L44 33 L37 42", SPINE) + lines([50], ASH, 19, 40, 0.4),
    "exec": f'<polygon points="32,22 44,46 20,46" fill="{MAGMA}"/><line x1="32" y1="29" x2="32" y2="45" stroke="{GROUND}" stroke-width="1.8"/>',
    "image": f'<rect x="19" y="23" width="26" height="22" fill="none" stroke="{SPINE}" stroke-width="1.6"/><path d="M19 45 L28 33 L33.5 40 L37.5 35.5 L45 45 Z" fill="{SPINE}"/>',
    "pdf": lines([23, 30]) + f'<rect x="12.5" y="38" width="39" height="10" fill="{BLAZE}"/>',
    "audio": stroke("M19 36 C22 25 25 47 29 36 C33 25 36 47 45 34", ASH),
    "video": f'<path d="M25 24 L43 35 L25 46 Z" fill="{ASH}"/>',
    "archive": f'<rect x="28.5" y="5.5" width="7" height="53" fill="{EMBER}"/><rect x="26" y="29" width="12" height="9" fill="{RAISED}" stroke="{MAGMA}" stroke-width="1.6"/>',
    "grid": stroke("M19 25 H45 M19 33 H45 M19 41 H45 M27.5 22 V47 M36.5 22 V47", ASH, 1.5),
    "slide": f'<rect x="19" y="23" width="26" height="16" fill="{EMBER}"/>' + stroke("M32 39 V48 M26 49 H38", ASH, 2),
    "font": stroke("M21 49 L32 23 L43 49 M25 40.5 H39", ASH),
}
DOCUMENTS = {
    None: ["application-x-generic", "unknown", "empty"],
    "text": ["text-x-generic", "text-plain", "x-office-document", "text-markdown", "text-x-readme"],
    "script": ["text-x-script", "application-x-shellscript", "text-x-python", "text-x-makefile"],
    "exec": ["application-x-executable", "application-x-sharedlib"],
    "image": ["image-x-generic"],
    "audio": ["audio-x-generic"],
    "video": ["video-x-generic"],
    "archive": ["package-x-generic", "application-x-archive", "application-zip", "application-x-compressed-tar", "application-x-tar"],
    "pdf": ["application-pdf"],
    "code": ["text-html", "application-json", "text-x-csrc", "text-x-c++src", "text-x-javascript"],
    "grid": ["x-office-spreadsheet"],
    "slide": ["x-office-presentation"],
    "font": ["font-x-generic"],
}
for kind, names in DOCUMENTS.items():
    write("scalable/mimetypes", svg64(sheet() + DOC_MARKS[kind]), names)


# ---- devices and trash -----------------------------------------------------------------
def box(x, y, w, h):
    a, b = 8, 4
    d = (f"M{x} {y + a} H{x + b} V{y + b} H{x + a} V{y} H{x + w} V{y + h - a} H{x + w - b} V{y + h - b} H{x + w - a} V{y + h} H{x} Z")
    return f'<path d="{d}" fill="{SLAG}" stroke="url(#edge)" stroke-width="1.5"/>'


def led(cx, cy):
    return f'<polygon points="{cx},{cy - 3.4} {cx + 3.2},{cy + 2.6} {cx - 3.2},{cy + 2.6}" fill="{MAGMA}"/>'


DRIVE = box(8.75, 21.75, 46.5, 22.5) + f'<rect x="16" y="32" width="20" height="2" fill="{EMBER}"/>' + led(46, 33)
write("scalable/devices", svg64(DRIVE), ["drive-harddisk", "drive-harddisk-system", "drive-multidisk"])
REMOVABLE = (f'<rect x="24.75" y="8.75" width="14.5" height="12" fill="{HAIR}" stroke="{MAGMA}" stroke-width="1.5"/>'
             + box(18.75, 20.75, 26.5, 35.5) + led(32, 40))
write("scalable/devices", svg64(REMOVABLE), ["drive-removable-media", "drive-harddisk-usb", "media-removable", "media-flash"])
OPTICAL = (f'<circle cx="32" cy="32" r="21.25" fill="{SLAG}" stroke="url(#edge)" stroke-width="1.5"/>'
           f'<path d="M32 18 A14 14 0 1 1 18 32" fill="none" stroke="{EMBER}" stroke-width="2"/>' + led(32, 32))
write("scalable/devices", svg64(OPTICAL), ["drive-optical", "media-optical"])
COMPUTER = box(9.75, 10.75, 44.5, 31.5) + stroke("M32 42.5 V53 M23 54 H41", MAGMA, 2) + led(32, 26.5)
write("scalable/devices", svg64(COMPUTER), ["computer", "video-display"])
BIN = (f'<path d="M17 20 H47 L43.5 58 H20.5 Z" fill="{SLAG}"/>' + stroke("M12 19.5 H52 M25 19.5 V11 H39 V19.5 M17 20 L20.5 58 H43.5 L47 20", MAGMA, 1.7)
       + stroke("M27 28 L28 50 M32 28 V50 M37 28 L36 50", EMBER, 1.5))
write("scalable/places", svg64(BIN), ["user-trash"])
write("scalable/places", svg64(BIN + f'<polygon points="32,2 38,12 26,12" fill="{MAGMA}"/>'), ["user-trash-full"])


# ---- 16px sidebar: plain line icons ------------------------------------------------------
SYM = {
    "home": '<path d="M2 8 L8 2.5 L14 8"/><path d="M4 7 V14 H12 V7"/>',
    "desktop": '<rect x="2" y="3" width="12" height="8"/><path d="M6 14 H10"/>',
    "documents": '<path d="M4 2 H10 L13 5 V14 H4 Z"/><path d="M6.5 8 H10.5 M6.5 11 H9.5"/>',
    "downloads": '<path d="M8 2 V11"/><path d="M4 7.5 L8 11.5 L12 7.5"/><path d="M3 14 H13"/>',
    "music": '<path d="M5.5 12.5 V3.5 L12.5 2.5 V11.5"/><circle cx="4" cy="12.5" r="1.6"/><circle cx="11" cy="11.5" r="1.6"/>',
    "pictures": '<path d="M2 13 L6 7 L9 10.5 L11 8.5 L14 13 Z"/><circle cx="11.5" cy="4.5" r="1.2"/>',
    "videos": '<path d="M5 3 V13 L13 8 Z"/>',
    "templates": '<rect x="2.5" y="2.5" width="11" height="11" stroke-dasharray="2.2 2"/>',
    "share": '<circle cx="4" cy="8" r="1.6"/><circle cx="12" cy="3.8" r="1.6"/><circle cx="12" cy="12.2" r="1.6"/><path d="M5.4 7.2 L10.6 4.6 M5.4 8.8 L10.6 11.4"/>',
    "folder": '<path d="M2 4 H6.5 L8 5.5 H14 V13 H2 Z"/>',
    "recent": '<circle cx="8" cy="8" r="6"/><path d="M8 4.5 V8 L10.5 9.5"/>',
    "trash": '<path d="M3 4.5 H13"/><path d="M6 4.5 V2.5 H10 V4.5"/><path d="M4.5 4.5 L5.5 14 H10.5 L11.5 4.5"/>',
    "bookmark": '<path d="M4 2 H12 V14 L8 10.5 L4 14 Z"/>',
    "drive": '<rect x="2" y="5" width="12" height="6"/><path d="M10.5 8 H11.5"/>',
    "removable": '<rect x="4.5" y="5" width="7" height="9"/><path d="M6 5 V2 H10 V5"/>',
    "optical": '<circle cx="8" cy="8" r="6"/><circle cx="8" cy="8" r="1.5"/>',
    "computer": '<rect x="2" y="2.5" width="12" height="8"/><path d="M5 14 H11 M8 10.5 V14"/>',
    "network": '<circle cx="8" cy="8" r="6"/><path d="M2 8 H14 M8 2 C5 5 5 11 8 14 M8 2 C11 5 11 11 8 14"/>',
}


def sym16(key):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none" '
            f'stroke="{SIDE}" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">{SYM[key]}</svg>\n')


SIDEBAR = {
    "places": {
        "home": ["user-home", "folder-home", "go-home"], "desktop": ["user-desktop"], "documents": ["folder-documents"],
        "downloads": ["folder-download"], "music": ["folder-music"], "pictures": ["folder-pictures"],
        "videos": ["folder-videos"], "templates": ["folder-templates"], "share": ["folder-publicshare"],
        "folder": ["folder", "inode-directory", "folder-open", "folder-drag-accept", "folder-visiting"],
        "recent": ["document-open-recent", "folder-recent"], "trash": ["user-trash", "user-trash-full"],
        "bookmark": ["user-bookmarks", "bookmark-new"], "network": ["folder-remote", "network-workgroup", "network-server"],
    },
    "devices": {
        "drive": ["drive-harddisk", "drive-harddisk-system", "drive-multidisk"],
        "removable": ["drive-removable-media", "drive-harddisk-usb", "media-removable", "media-flash"],
        "optical": ["drive-optical", "media-optical"], "computer": ["computer", "video-display"],
    },
}
for ctx, groups in SIDEBAR.items():
    for key, names in groups.items():
        write(f"16/{ctx}", sym16(key), names)

(ROOT / "index.theme").write_text(f"""[Icon Theme]
Name={NAME}
Comment=Kaiju: terraced Ember plates for folders, Ash outlines for documents, plain 16px line icons
Inherits=Adwaita,hicolor
Example=folder

Directories=16/places,16/devices,scalable/places,scalable/mimetypes,scalable/devices

[16/places]
Size=16
Context=Places
Type=Fixed

[16/devices]
Size=16
Context=Devices
Type=Fixed

[scalable/places]
Size=64
MinSize=20
MaxSize=512
Context=Places
Type=Scalable

[scalable/mimetypes]
Size=64
MinSize=16
MaxSize=512
Context=MimeTypes
Type=Scalable

[scalable/devices]
Size=64
MinSize=20
MaxSize=512
Context=Devices
Type=Scalable
""")
subprocess.run(["gtk-update-icon-cache", "-f", "-t", str(ROOT)], check=False,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"{NAME} icons written to {ROOT}")

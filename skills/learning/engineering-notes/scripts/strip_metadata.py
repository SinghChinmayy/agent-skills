#!/usr/bin/env python3
"""Remove EXIF, XMP and comment metadata from JPEG photos, in place.

Phone photos can carry GPS coordinates, device details and timestamps.
Notebook pages are published, so run this on every photo before it is
committed. Standard library only.

    python3 scripts/strip_metadata.py notes/<subject>/sources/*.jpg

Keeps the JFIF header (APP0) and the colour profile (APP2 ICC), and drops
every other APPn segment and comments. It refuses photos whose EXIF says
they are stored rotated, since dropping that tag would turn them sideways;
rotate those first (for example `sips -r 90 photo.jpg` on macOS).
"""

import sys
from pathlib import Path

KEEP = {0xE0, 0xE2}  # APP0 (JFIF), APP2 (ICC colour profile)


def has_metadata(data: bytes) -> bool:
    """True if a JPEG has any APPn segment other than APP0/APP2, or a comment."""
    return any(marker not in KEEP for marker, _ in segments(data) if 0xE1 <= marker <= 0xEF or marker == 0xFE)


def segments(data: bytes):
    """Yield (marker, segment bytes) for header segments up to the image data."""
    if data[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG file")
    i = 2
    while i < len(data) - 4 and data[i] == 0xFF:
        marker = data[i + 1]
        if marker == 0xDA:  # start of scan: the rest is image data
            return
        length = int.from_bytes(data[i + 2:i + 4], "big")
        yield marker, data[i:i + 2 + length]
        i += 2 + length


def rotated(segment: bytes) -> bool:
    """True if an EXIF segment holds an orientation other than 1 (upright)."""
    body = segment[4:]
    if not body.startswith(b"Exif\x00\x00"):
        return False
    tiff = body[6:]
    big = tiff[:2] == b"MM"
    read = lambda b: int.from_bytes(b, "big" if big else "little")
    ifd = read(tiff[4:8])
    for n in range(read(tiff[ifd:ifd + 2])):
        entry = tiff[ifd + 2 + 12 * n: ifd + 14 + 12 * n]
        if read(entry[:2]) == 0x0112:  # Orientation
            return read(entry[8:10]) != 1
    return False


def strip(path: Path) -> None:
    data = path.read_bytes()
    kept, removed, end = [data[:2]], 0, 2
    for marker, segment in segments(data):
        end += len(segment)
        if marker == 0xE1 and rotated(segment):
            raise ValueError(f"{path}: EXIF says the photo is rotated; rotate it upright first")
        if (0xE1 <= marker <= 0xEF and marker not in KEEP) or marker == 0xFE:
            removed += 1
            continue
        kept.append(segment)
    path.write_bytes(b"".join(kept) + data[end:])
    print(f"{path}: removed {removed} metadata segment(s)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for name in sys.argv[1:]:
        strip(Path(name))

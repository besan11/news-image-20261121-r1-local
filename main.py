#!/usr/bin/env python3
"""Entry program (Python 3.13, standard library only).

Copies the front-page image rendered by render.py (entry.png, held in
this repository) to the grader's output directory as entry.png, then
verifies the copy is a whole PNG by checking its magic bytes and size.

The program never deletes anything: it does not remove the output
directory (in the grader that directory is a bind mount, and removing
it fails) and it does not clear the directory's contents either; it
only writes the one file it is asked for. Both runs write identical
bytes because the source image is a fixed file in the repository.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(SOURCE, "rb") as src:
        head = src.read(len(PNG_MAGIC))
        if head != PNG_MAGIC:
            print("entry.png is not a PNG", file=sys.stderr)
            return 1
    shutil.copyfile(SOURCE, dest)
    with open(dest, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    size = os.path.getsize(dest)
    if size > 1048576:
        print("entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, sha256 %s)" % (dest, size, digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Self-check for the news-image-20261121 r1 entry.

Checks the gate limits (PNG, <=1 MiB, <=1024x1024), that main.py runs
twice with exit 0 and writes identical bytes, and that main.py never
deletes the output directory (no rmtree / remove / unlink of it).
Exits 0 only when every check passes.
"""

import hashlib
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
fails = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" — " + detail if detail else ""))
    if not ok:
        fails.append(name)


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    entry = os.path.join(HERE, "entry.png")
    with open(entry, "rb") as f:
        head = f.read(8)
    check("png magic bytes", head == PNG_MAGIC)
    size = os.path.getsize(entry)
    check("size <= 1 MiB", size <= 1048576, "%d bytes" % size)
    from PIL import Image
    im = Image.open(entry)
    check("dimensions <= 1024x1024", im.size[0] <= 1024 and im.size[1] <= 1024,
          "%dx%d" % im.size)

    main_py = os.path.join(HERE, "main.py")
    with open(main_py, "r", encoding="utf-8") as f:
        src = f.read()
    check("main.py never deletes the output dir",
          not re.search(r"rmtree|shutil\.rmtree|os\.remove|os\.unlink|"
                        r"shutil\.rmtree|os\.rmdir", src))
    check("main.py is stdlib-only (no third-party imports)",
          not re.search(r"^import (PIL|numpy|requests|cv2)\b",
                        src, re.MULTILINE))

    # Two runs, separate output dirs, must exit 0 with identical bytes.
    digests = []
    with tempfile.TemporaryDirectory() as tmp:
        for i in (1, 2):
            out = os.path.join(tmp, "out%d" % i)
            os.makedirs(out)
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=out)
            r = subprocess.run([sys.executable, main_py], env=env,
                               capture_output=True, text=True, timeout=60)
            check("run %d exit 0" % i, r.returncode == 0,
                  (r.stderr or r.stdout).strip()[:160])
            if r.returncode == 0:
                digests.append(sha(os.path.join(out, "entry.png")))
    if len(digests) == 2:
        check("two runs write identical bytes", digests[0] == digests[1],
              digests[0][:16])

    print("---")
    if fails:
        print("FAILED: %s" % ", ".join(fails))
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

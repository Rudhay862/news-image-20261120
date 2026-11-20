#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261120.

Copies the bundled entry.png (the 20 November 2026 world-news front page)
to /output/entry.png. Standard library only, no network, deterministic:
both runs write the same bytes.
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
EXPECTED_SHA256 = "3c44d97cd06bd5cb30b265f085a475ac49c471682ad7c82ef82daa2a61d76a06"

OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    data = open(SRC, "rb").read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit("entry.png sha256 mismatch: %s" % digest)
    os.makedirs(OUT_DIR, exist_ok=True)
    # Clear the output directory's contents only; never remove the
    # directory itself (the grader user may not be able to recreate it).
    for name in os.listdir(OUT_DIR):
        path = os.path.join(OUT_DIR, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    out = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(SRC, out)
    print("wrote %s (%d bytes)" % (out, len(data)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Copy the committed entry.png to the make.fun output directory.

Reads the output directory from MAKEFUN_OUTPUT_DIR when set, otherwise
/output. Creates the directory if needed, copies entry.png byte for
byte, and prints the destination path and byte size. Standard library
only; no network, nothing generated at run time.
"""

import hashlib
import os
import shutil
import sys


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, dest)
    size = os.path.getsize(dest)
    if _sha256(source) != _sha256(dest):
        print(f"error: copied file failed byte-for-byte check: {dest}",
              file=sys.stderr)
        return 1
    print(f"{dest} {size} bytes (verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

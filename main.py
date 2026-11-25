#!/usr/bin/env python3
"""Copy the committed entry.png to the make.fun output directory.

Reads the output directory from MAKEFUN_OUTPUT_DIR when set, otherwise
/output. Creates the directory if needed, copies entry.png byte for
byte, and prints the destination path and byte size. Standard library
only; no network, nothing generated at run time.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, dest)
    size = os.path.getsize(dest)
    print(f"{dest} {size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

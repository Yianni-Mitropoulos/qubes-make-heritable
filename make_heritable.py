#!/usr/bin/env python3

import os
import shutil
import sys
from pathlib import Path

def error(msg):
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(1)

def main():
    if len(sys.argv) != 2:
        error("Usage: make-heritable <file-or-directory-relative-to-cwd>")

    input_path = Path(sys.argv[1]).expanduser()
    abs_src = input_path.resolve()

    cwd = Path.cwd().resolve()
    try:
        rel_path = abs_src.relative_to(cwd)
    except ValueError:
        error(f"The path {abs_src} is not under the current working directory {cwd}")

    dest_path = Path('/etc/skel') / rel_path

    if not abs_src.exists():
        error(f"Source path does not exist: {abs_src}")

    print(f"Copying: {abs_src} → {dest_path}")

    # Ensure destination parent directory exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # Remove existing destination if needed
    if dest_path.exists():
        if dest_path.is_dir():
            shutil.rmtree(dest_path)
        else:
            dest_path.unlink()

    try:
        if abs_src.is_dir():
            shutil.copytree(abs_src, dest_path)
        else:
            shutil.copy2(abs_src, dest_path)
        print("✅ Successfully copied to /etc/skel/")
    except Exception as e:
        error(f"Copy failed: {e}")

    print("ℹ️  This change will apply to newly created AppVMs from this template.")

if __name__ == "__main__":
    main()

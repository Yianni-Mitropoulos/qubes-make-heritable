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
        error("Usage: qubes_skel_copy.py <relative-path-from-home>")

    rel_path = sys.argv[1]
    if rel_path.startswith('/') or '..' in rel_path:
        error("Please provide a safe, relative path from your home directory (no leading / or ..)")

    home = Path.home()
    src = home / rel_path
    dest = Path('/etc/skel') / rel_path

    if not src.exists():
        error(f"Source path does not exist: {src}")

    print(f"Copying: {src} → {dest}")

    # Ensure parent directories exist in /etc/skel
    dest.parent.mkdir(parents=True, exist_ok=True)

    # Remove destination if it already exists
    if dest.exists():
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()

    try:
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
        print("✅ Copy completed successfully.")
    except Exception as e:
        error(f"Failed to copy: {e}")

    print("Note: These changes will be reflected in *new* AppVMs created from this template.")

if __name__ == "__main__":
    main()

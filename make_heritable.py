#!/usr/bin/env python3

import os
import shutil
import sys
from pathlib import Path

def error(msg):
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(1)

def warn(msg):
    print(f"[WARNING] {msg}", file=sys.stderr)

def copy_to_skel(src: Path, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
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
        print(f"✅ Copied {src} → {dest}")
    except Exception as e:
        warn(f"Copy failed for {src}: {e}")

def do_firefox():
    mozilla = Path.home() / ".mozilla" / "firefox"
    profiles_ini = mozilla / "profiles.ini"
    if not profiles_ini.exists():
        error("profiles.ini not found. Has Firefox run yet?")

    # Copy profiles.ini
    skel_profiles_ini = Path("/etc/skel/.mozilla/firefox/profiles.ini")
    copy_to_skel(profiles_ini, skel_profiles_ini)

    # Find default profile directory
    default_profile = None
    profile_dir = None
    with profiles_ini.open() as f:
        lines = f.readlines()
    current = {}
    for line in lines:
        line = line.strip()
        if line.startswith("[Profile"):
            current = {}
        elif "=" in line:
            k, v = line.split("=", 1)
            current[k.strip()] = v.strip()
        if current.get("Default") == "1":
            default_profile = current.get("Path")
    if not default_profile:
        error("Could not determine default profile from profiles.ini")
    profile_dir = mozilla / default_profile
    if not profile_dir.exists():
        error(f"Default profile directory not found: {profile_dir}")

    # List of files to copy from profile dir
    for fname in ["prefs.js", "user.js", "search.json.mozlz4"]:
        src = profile_dir / fname
        dest = Path("/etc/skel/.mozilla/firefox") / default_profile / fname
        if src.exists():
            copy_to_skel(src, dest)
        else:
            warn(f"File not found and skipped: {src}")

    print("🦊 Firefox essential settings copied to /etc/skel/.mozilla/firefox/")
    print("ℹ️  This will affect new AppVMs created from this TemplateVM.")

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--firefox":
        do_firefox()
        return

    if len(sys.argv) != 2:
        error("Usage: make-heritable <file-or-directory-relative-to-cwd> OR make-heritable --firefox")

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

    dest_path.parent.mkdir(parents=True, exist_ok=True)
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

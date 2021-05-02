#!/usr/bin/python3
# Unpack Moodle Rust homework submissions for grading.
# Bart Massey 2021

import os, pathlib, shutil, sys, zipfile
from pathlib import Path

submissions = Path("orig")
ungraded = Path("staged")

assert len(sys.argv) == 3
assignment = sys.argv[1]
ziporig = sys.argv[2]

def canon_name(name):
    return '-'.join(name.lower().split())

# https://stackoverflow.com/a/1724723
def find_cargo(gpath):
    result = []
    for root, dirs, files in os.walk(gpath):
        if "Cargo.toml" in files:
            result.append(Path(root))
    return result

def pull_up(gpath):
    actuals = find_cargo(gpath)
    if len(actuals) != 1:
        print(f"{gpath}: cannot pull up ({actuals})", file=sys.stderr)
        return False
    actual = actuals[0]
    for obj in actual.iterdir():
        obj.rename(gpath / obj.name)
    killme = Path('.').joinpath(*actual.parts[:3])
    for root, dirs, files in os.walk(killme):
        if len(files) > 0:
            print(f"{gpath}: warning: files remaining", file=sys.stderr)
            return True
    shutil.rmtree(killme)
    return True

shutil.rmtree(submissions, ignore_errors=True)
submissions.mkdir()
ungraded.mkdir()

with zipfile.ZipFile(ziporig) as zips:
    zips.extractall(path=submissions)

for student in sorted(submissions.iterdir()):
    ss = str(student.name)
    endname = ss.index('_')
    assert endname > 0
    name = ss[:endname]
    cname = canon_name(name)

    zipfiles = list(student.glob("*.zip"))
    if len(zipfiles) == 0:
        print(f"{name}: empty", file=sys.stderr)
        continue
    elif len(zipfiles) > 1:
        print(f"{name}: multiple zipfiles", file=sys.stderr)
        continue
    hwzip = zipfiles[0]

    gdir = ungraded / Path(cname)
    gdir.mkdir()

    with zipfile.ZipFile(hwzip) as zips:
        zips.extractall(path=gdir)

    if not (gdir / Path("Cargo.toml")).is_file():
        if not pull_up(gdir):
            continue

    main_file_path = Path("main.rs")
    main_path = gdir / main_file_path
    if main_path.is_file():
        print(f'"correcting" {cname}: top-level main.rs')
        src_path = gdir / Path("src")
        if not src_path.is_dir():
            src_path.mkdir()
        main_path.rename(gdir / Path("src") / main_file_path)
        
    with open(gdir / "GRADING.txt", "w") as g:
        print(f"{assignment}\n{name}\n?\n", file=g)

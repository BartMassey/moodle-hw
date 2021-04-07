#!/usr/bin/python3
# Unpack Moodle Rust homework submissions for grading.
# Bart Massey 2021

submissions = Path("orig")
ungraded = Path("staged")

import os, pathlib, shutil, subprocess, sys
from pathlib import Path

assert len(sys.argv) == 3
assignment = sys.argv[1]
zipfile = sys.argv[2]

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
    # print("rm -r", killme)
    shutil.rmtree(killme)
    return True

shutil.rmtree(submissions, ignore_errors=True)
submissions.mkdir()
# XXX Remove this next line!
shutil.rmtree(ungraded, ignore_errors=True)
ungraded.mkdir()

subprocess.run(
    ["unzip", "-d", submissions, "-x", zipfile],
    stdout=subprocess.DEVNULL,
)
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
    subprocess.run(
        ["unzip", "-d", gdir, "-x", hwzip],
        stdout=subprocess.DEVNULL,
    )
    if not (gdir / Path("Cargo.toml")).is_file():
        if not pull_up(gdir):
            continue
        
    with open(gdir / "GRADING.txt", "w") as g:
        print(f"{assignment}\n{name}\n?\n", file=g)

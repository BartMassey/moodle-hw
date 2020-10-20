#!/usr/bin/python3

import argparse, os, re, subprocess, sys
from collections import defaultdict

ap = argparse.ArgumentParser()
ap.add_argument(
    "--pdf",
    help="Assignments are PDF files",
    action="store_true",
)
ap.add_argument(
    "--html",
    help="Assignments are online text HTML files",
    action="store_true",
)
ap.add_argument(
    "-t", "--title",
    help="Assignment title",
)
ap.add_argument(
    "-p", "--project",
    help="Assignment is group project",
    action="store_true",
)
args = ap.parse_args()
if args.title is not None and args.project:
    print("assignment or project?", file=sys.stderr)
    exit(1)
if args.title is None and not args.project:
    print("no assignment title", file=sys.stderr)
    exit(1)
if args.pdf and args.html:
    print("pdf or html?", file=sys.stderr)
    exit(1)

if not os.path.isdir("orig"):
    print("no orig", file=sys.stderr)
    exit(1)

if os.path.isdir("staged"):
    print("staged exists", file=sys.stderr)
    exit(1)

ws_re = re.compile(" +")
def canon(title):
    xtitle = ws_re.sub("-", title)
    return xtitle.lower()

front_re = re.compile("_.*")
authors = defaultdict(lambda: [])
transfers = dict()
for d in os.listdir("orig"):

    sd = os.path.join("orig", d)
    contents = list(os.listdir(sd))
    if len(contents) == 0:
        continue
    if len(contents) > 1:
        print(f"{sd}: multiple files", file=sys.stderr)
        continue
    sf = os.path.join(sd, contents[0])

    desc = front_re.sub("", d)
    if args.project:
        title, author = desc.split('-')
        target = canon(title)
        authors[target].append(author)
    else:
        title = args.title
        author = desc
        target = canon(author)
    dd = os.path.join("staged", target)

    transfers[target] = (sf, dd, title, author)

os.mkdir("staged")
for target in transfers:
    sf, dd, title, author = transfers[target]
    if args.project:
        author = ", ".join(authors[target])

    os.mkdir(dd)
    if args.pdf:
        subprocess.run(["cp", sf, f"{dd}/assignment.pdf"])
    elif args.html:
        subprocess.run(["cp", sf, f"{dd}/assignment.html"])
    else:
        subprocess.run(["unzip", "-x", "-q", f"../../{sf}"], cwd=dd)

    grf = os.path.join(dd, "GRADING.txt")
    with open(grf, "w") as gr:
        print(f"{title}\n{author}\n-\n", file=gr)


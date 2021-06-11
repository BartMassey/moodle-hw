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

base = "staged"
if os.path.isdir(base):
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
    sfs = [os.path.join(sd, c) for c in contents]
    if len(contents) > 1:
        print(f"{sd}: warning: multiple files", file=sys.stderr)

    desc = front_re.sub("", d)
    if args.project:
        last_space = desc.rindex(' ')
        prefix = desc[:last_space]
        last_dash = prefix.rindex('-')
        title = desc[:last_dash]
        author = desc[last_dash + 1:]
        target = canon(title)
        authors[target].append(author)
    else:
        title = args.title
        author = desc
        target = canon(author)
    dd = os.path.join(base, target)

    transfers[target] = (sfs, dd, title, author)

os.mkdir(base)
for target in transfers:
    sfs, dd, title, author = transfers[target]
    if args.project:
        author = ", ".join(authors[target])

    os.mkdir(dd)
    if len(sfs) > 1:
        subprocess.run(["cp", *sfs, f"{dd}/"])
    elif args.pdf:
        subprocess.run(["cp", sfs[0], f"{dd}/assignment.pdf"])
    elif args.html:
        subprocess.run(["cp", sfs[0], f"{dd}/assignment.html"])
    else:
        subprocess.run(["unzip", "-x", "-q", f"../../{sfs[0]}"], cwd=dd)

    grf = os.path.join(dd, "GRADING.txt")
    with open(grf, "w") as gr:
        print(f"{title}\n{author}\n-\n", file=gr)


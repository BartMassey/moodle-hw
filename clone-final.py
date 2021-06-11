#!/usr/bin/python3

import argparse, csv, os.path, re, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument(
    "-u", "--url-file",
    help="repo urls file",
)
ap.add_argument(
    "-d", "--dry-run",
    help="show actions rather than perform them",
    action="store_true",
)
args = ap.parse_args()

urls = csv.reader(open(args.url_file, "r"))
headers = next(urls)
assert list(headers) == ["ctitle", "title", "url"]

def sh(cmdargs):
    if args.dry_run:
        print(*cmdargs)
    else:
        subprocess.run(cmdargs)

ws_re = re.compile(" +")
def canon(title):
    xtitle = ws_re.sub("-", title)
    xtitle = xtitle.replace("'", "")
    return xtitle.lower()

base = "staged"
for ctitle, title, url in urls:
    path = os.path.join(base, ctitle, "repo")
    sh(["git", "clone", url, path])

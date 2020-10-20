#!/usr/bin/python3

import argparse, csv, os, re, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument(
    "-u", "--url-file",
    help="repo urls file",
    default="../progress-review/urls.csv",
)
ap.add_argument(
    "-p", "--projects-file",
    help="projects info file",
    default="../proposal/groups.csv",
)
ap.add_argument(
    "-d", "--dry-run",
    help="show actions rather than perform them",
    action="store_true",
)
args = ap.parse_args()

urls = csv.reader(open(args.url_file, "r"))
headers = next(urls)
assert list(headers) == ["title", "url", "branch"]
projects = csv.reader(open(args.projects_file, "r"))
headers = next(projects)
assert list(headers) == [
    "username", "firstname", "lastname",
    "email", "course1", "group1",
]

groups = dict()
for _, firstname, lastname, _, _, title in projects:
    name = f"{firstname} {lastname}"
    groups.setdefault(title, []).append(name)

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

os.mkdir("staged")
os.chdir("staged")

for title, url, branch in urls:
    authors = ", ".join(sorted(groups[title]))
    path = canon(title)
    sh(["git", "clone", url, path])
    if args.dry_run:
        continue

    os.chdir(path)
    if branch != "master":
        sh(["git", "checkout", branch])
    with open("GRADING.txt", "w") as gr:
        print(f"{title}\n{authors}\n-\n", file=gr)
    os.chdir("..")

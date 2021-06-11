#!/usr/bin/python3

import csv, os, re, sys

url_re = re.compile(
    "https?://git[-_/.a-zA-Z0-9]+"
)

w = csv.writer(sys.stdout)
w.writerow(["ctitle", "title", "url"])
base = "staged"
for d in os.listdir(base):
    gr = os.path.join(base, d, "GRADING.txt")
    with open(gr, "r") as grf:
        name = next(grf).strip()
    asg = os.path.join(base, d, "assignment.html")
    with open(asg, "r") as asgf:
        url = None
        for line in asgf:
            match = url_re.search(line)
            if match != None:
                url = match.group()
                break
    w.writerow([d, name, url])

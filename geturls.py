#!/usr/bin/python3

import os, re, sys

url_re = re.compile(
    "https?://git[-_/.a-zA-Z0-9]+"
)

for d in os.listdir("."):
    gr = os.path.join(d, "GRADING.txt")
    with open(gr, "r") as grf:
        name = next(grf).strip()
    asg = os.path.join(d, "assignment.html")
    with open(asg, "r") as asgf:
        url = None
        for line in asgf:
            match = url_re.search(line)
            if match != None:
                url = match.group()
                break
    print(f"{name},{url}")

#!/usr/bin/python3
import csv

r = csv.reader(open("groups.csv", "r"))
headers = next(r)
h = {headers[i] : i for i in range(len(headers))}

groups = dict()
for fields in r:
    first = fields[h["firstname"]]
    last = fields[h["lastname"]]
    groups.setdefault(fields[h["group1"]], []).append(f"{first} {last}")

for g in groups:
    print(f"{g}: {', '.join(groups[g])}")

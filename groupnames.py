#!/usr/bin/python3
# Extract moodle group names (not usernames) from groups.csv

import csv, sys

groups = csv.reader(open("groups.csv", "r"))
fields = next(groups)
idxs = {fields[i] : i for i in range(len(fields))}
idx = idxs["group1"]
groupnames = {fields[idx] for fields in groups}

mgroups = csv.writer(sys.stdout)
mgroups.writerow(["groupname", "groupingname"])
for name in groupnames:
    mgroups.writerow([name, "Project"])

#!/usr/bin/python3
# Extract moodle group member names from groups.csv

import csv, sys

course = sys.argv[1]

groups = csv.reader(open("groups.csv", "r"))
fields = next(groups)
idxs = {fields[i] : i for i in range(len(fields))}
group_idx = idxs["group1"]
firstname_idx = idxs["firstname"]
lastname_idx = idxs["lastname"]
membership = {
    f"{fields[firstname_idx]} {fields[lastname_idx]}" : fields[group_idx]
    for fields in groups
}

students = csv.reader(open("students.csv", "r"))
fields = next(students)
idxs = {fields[i] : i for i in range(len(fields))}
firstname_idx = idxs["firstname"]
lastname_idx = idxs["lastname"]
username_idx = idxs["username"]
email_idx = idxs["email"]
enrolment = dict()
for student in students:
    firstname = student[firstname_idx]
    lastname = student[lastname_idx]
    username = student[username_idx]
    email = student[email_idx]
    name = f"{firstname} {lastname}"
    enrolment[name] = (firstname, lastname, username, email)

missing = False
for (name, groupname) in membership.items():
    if name not in enrolment:
        print("not found:", name, groupname, file=sys.stderr)
        missing = True

if missing:
    exit(1)

musers = csv.writer(sys.stdout)
musers.writerow(["firstname", "lastname", "username", "email", "course1", "group1"])
for (name, groupname) in membership.items():
    (firstname, lastname, username, email) = enrolment[name]
    musers.writerow([firstname, lastname, username, email, course, groupname])

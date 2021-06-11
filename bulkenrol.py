#!/usr/bin/python3

import csv, sys

f = open(sys.argv[1], 'r')
reader = csv.reader(f)
headers = next(reader)
if len(headers) == 5:
    assert headers == [
        "username", "firstname", "lastname", "nickname", "email",
    ]
    for username, firstname, lastname, nickname, email in reader:
        print(email)
else:
    assert headers == [
        "username", "firstname", "lastname", "nickname", "email", "course1",
    ]

    sections = dict()
    for username, firstname, lastname, nickname, email, course in reader:
        sections.setdefault(course, [])
        sections[course].append(email)

    output = list()
    for section in sections:
        output.append("# " + section)
        for email in sections[section]:
            output.append(email)
    print('\n'.join(output))

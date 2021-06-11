#!/usr/bin/python3

import csv, re, sys

f = open(sys.argv[1], 'r')
reader = csv.reader(f)
headers = next(reader)

if len(headers) == 5:
    assert headers == [
        "username", "firstname", "lastname", "nickname", "email",
    ]
else:
    assert headers == [
        "username", "firstname", "lastname", "nickname", "email", "course1",
    ]

writer = csv.writer(sys.stdout)
writer.writerow(["username", "firstname", "lastname", "email"])

if len(headers) == 5:
    for username, firstname, lastname, nickname, email in reader:
        writer.writerow([username, firstname, lastname, email])
else:
    for username, firstname, lastname, nickname, email, course in reader:
        writer.writerow([username, firstname, lastname, email])
        

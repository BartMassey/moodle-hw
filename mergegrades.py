#!/usr/bin/python3

import argparse, csv, os, sys

ap = argparse.ArgumentParser()
ap.add_argument(
    "-w", "--worksheet",
    help="Moodle CSV grading worksheet",
    default="grades-moodle.csv",
)
ap.add_argument(
    "-o", "--annotated",
    help="Annotated Moodle CSV grading worksheet",
    default="annotated-grades-moodle.csv",
)
ap.add_argument(
    "-d", "--graded",
    help="Directory of graded content",
    default="graded",
)
ap.add_argument(
    "-g", "--groups",
    help="Generated group list for Moodle.",
    default="groups.csv",
)
ap.add_argument(
    "-G", "--groupings",
    help="Generated groupings list for Moodle.",
    default="groupings.csv",
)
ap.add_argument(
    "-t", "--group-title",
    help="Grading title for alt group members.",
)
ap.add_argument(
    "-c", "--course",
    help="Course shortname for group title.",
)
args = ap.parse_args()
if args.group_title is None:
    args.groups = None
    args.groupings = None
if args.groups is not None and args.course is None:
    print("no course for groups file", file=sys.stderr)
    exit(1)

def stripname(a):
    return a.replace("'", "")

wsf = open(args.worksheet, "r", encoding='utf-8-sig')
ws = csv.reader(wsf)
rawheaders = next(ws)
headers = dict([(j, i) for i, j in enumerate(rawheaders)])
entries = { stripname(row[headers["Full name"]]) : row for row in ws
            if row[headers["Status"]].startswith("Submitted") }

grades = dict()
alts = set()
groups = dict()
for d in os.listdir(args.graded):
    fname = os.path.join(args.graded, d, "GRADING.txt")
    with open(fname, "r") as g:
        excepted = False
        try:
            title = next(g).strip()
            groupalt = args.group_title == title
            authors = next(g).strip()
            scoretext = next(g).strip()
            if groupalt:
                if scoretext != "":
                    excepted = True
            else:
                score = int(scoretext)
        except Exception as e:
            excepted = True
        if title == "" or authors == "" or excepted:
            print(
                f"{fname}: malformed header",
                file=sys.stderr,
            )
            continue
        authors = authors.split(", ")
        if scoretext != "":
            sep = next(g).strip()
            if sep != "":
                print(
                    f"warning: {fname}: separator was {sep}",
                    file=sys.stderr,
                )
                continue
        if groupalt:
            if len(authors) == 1:
                alts.add(authors[0])
            else:
                print(
                    f"warning: group alt with weird authors {', '.join(authors)}",
                    file = sys.stderr,
                )
            continue
        comments = g.read()
        groups[title] = authors
        for author in authors:
            grades[author] = (score, comments)

for a in alts:
    if a not in grades:
        print(
            f"warning: unassigned group alt {a}",
            file=sys.stderr,
        )

def paragraphs(txt):
    pars = txt.strip().split("\n\n")
    return "\n\n".join([par.strip().replace("\n", " ") for par in pars])

for author in grades:
    if author not in entries:
        print(f"{author} not found", file=sys.stderr)
        continue
    score, comments = grades[author]
    entries[author][headers["Grade"]] = str(score)
    entries[author][headers["Feedback comments"]] = paragraphs(comments)

with open(args.annotated, "w") as gs:
    out = csv.writer(gs)
    out.writerow(rawheaders)
    for row in entries.values():
        out.writerow(row)

if args.groups is not None:
    course = args.course

    with open(args.groups, "w") as gr:
        out = csv.writer(gr)
        out.writerow([
            "username",
            "firstname",
            "lastname",
            "email",
            "course1",
            "group1",
        ])
        for g in groups:
            for a in groups[g]:
                e = entries[a]
                firstname, lastname = e[headers["Full name"]].split(' ')
                email = e[headers["Email address"]]
                username, _ = email.split('@')
                out.writerow([username, firstname, lastname, email, course, g])

    with open(args.groupings, "w") as gr:
        out = csv.writer(gr)
        out.writerow([
            "groupname",
            "groupingname",
        ])
        for g in groups:
            out.writerow([g, args.group_title])

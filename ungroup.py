#!/usr/bin/python3
# Bart Massey

# Reconstruct and repack the zip archive produce by Moodle for group
# projects into something cromulent for grading.

import os, shlex

zipfiles = dict()
authors = dict()

for d in os.listdir("orig"):
    info = d.split('_')[0]
    splitpoint = info.rindex('-')
    proj = info[:splitpoint]
    name = info[splitpoint+1:]

    if proj not in zipfiles:
        [zipf] = list(os.listdir(f"orig/{d}"))
        zipfiles[proj] = f"orig/{d}/{zipf}"

        authors[proj] = [name]
    else:
        authors[proj].append(name)

try:
    os.mkdir('graded')
except FileExistsError:
    pass

top = os.getcwd()
for proj in zipfiles:
    lastlower = '-'.join([n.split(' ')[-1].lower() for n in authors[proj]])
    target = f'graded/{lastlower}'
    try:
        os.mkdir(target)
    except FileExistsError:
        print(f"skipped existing {target}")
        continue
    os.chdir(target)

    zipf = zipfiles[proj]
    cmd = f"unzip -q -x ../../{shlex.quote(zipf)}"
    os.system(cmd)

    with open("GRADING.txt", "w") as gradef:
        print(proj, file=gradef)
        print(', '.join(authors[proj]), file=gradef)
        print(file=gradef)
        print(file=gradef)

    os.chdir(top)

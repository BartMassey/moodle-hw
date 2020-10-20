# moodle-hw: Tools for doing bulk grading with Moodle
Bart Massey

These Python tools form a poorly-written poorly-tested
poorly-documented toolsuite for managing bulk remote Moodle
class grading of assigments including group assignments and
projects.

Workflow is roughly:

* Set up the remote work on Moodle with the `offline grade
  worksheet` option.

* Download the zipball of student assignments and the
  offline grade worksheet

* Run `unpack.py` with appropriate options to create a
  `staged/` directory containing assignments to grade. Each
  top-level directory will have a `GRADING.txt` file that
  can be edited for feedback and score.

* Grade the projects one at a time, moving them from
  `staged/` to `graded/` as they are completed.

* Run `mergegrades.py` with appropriate options to fill in
  the offline grade worksheet with grades and feedback
  extracted from the `graded/` directories.

* Upload the offline grade worksheet to Moodle.

Group project workflow:

* Run `ungroup.py` if needed to reorganize everything for
  group grading.

* `grouplist.py` will try to build a group list suitable for
  uploading to the Moodle, starting with `groups.csv` which
  contains *[something I can't remember]*

Github project workflow:

* This software can be used in the situation
  in which work is submitted to the Moodle as Github
  URLs. `geturls.py`
  will extract the necessary Github URLs from Moodle
  submissions and set up the grading structure. `clone.py`
  can be used to clone the actual repos from the URLs.

# moodle-hw: Tools for doing bulk grading with Moodle
Bart Massey

These Python tools form a poorly-written poorly-tested
poorly-documented toolsuite for managing bulk remote Moodle
class grading of assigments including group assignments and
projects.

## Basic workflow

* Set up the remote work on Moodle with the `offline grade
  worksheet` option.

* Download the zipball of student assignments and the
  offline grade worksheet

* Grotty shell-ish way:

    * Make an `orig` directory and `unzip` the zipball of
      student assignments into it.

    * Run `unpack.py` with appropriate options to create a
      `staged/` directory containing assignments to grade. Each
      top-level directory will have a `GRADING.txt` file that
      can be edited for feedback and score.

* For grading Rust homework (looks for a `Cargo.toml` file):

    * Run `unpack-rust-hw.py` with the assignment name and
      zipfile name as arguments.

    * Make an empty `graded/` directory.

* Grade the projects one at a time, moving them from
  `staged/` to `graded/` as they are completed. Edit
  each `GRADING.txt` as appropriate.

* Run `mergegrades.py` with appropriate options to fill in
  the offline grade worksheet with grades and feedback
  extracted from the `graded/` directories.

* Upload the offline grade worksheet to Moodle.

## Group project workflow

* Run `ungroup.py` if needed to reorganize everything for
  group grading.

* `grouplist.py` will try to build a group list suitable for
  uploading to the Moodle, starting with `groups.csv` which
  contains *[something I can't remember]*

## Github project workflow

This software can be used in the situation in which work
is submitted to the Moodle as Github URLs.

* `geturls.py` will directly extract the necessary Github
  URLs from Moodle submissions and set up the grading
  structure.

* `clone.py` can be used to clone the actual repos from the
  URLs in the case where projects and their URLs are being
  drawn from previous submissions.

* `clone-final.py` works directly from the CSV file produced
  by `geturls.py` to clone projects.

* `mergegrades.py` can just be used directly as normal on
  the graded output.

## Course / project enrolment workflow

`bulkenrol.py`, `bulkreg.py`, `groupnames.py`,
`groupmembers.py` are tools for dealing with course and
project setup.

#!/bin/sh
if [ $# -eq 0 ]
then
    echo "no title" >&2
    exit 1
fi
if ! [ -d orig ]
then
    echo "no orig" >&2
    exit 1
fi
if [ -d staged ]
then
    echo "staged directory exists" >&2
    exit 1
fi
mkdir staged
cd orig
for d in *
do
    NAME="`echo \"$d\" | sed 's/_[0-9].*//'`"
    LCNAME="`echo \"$NAME\" | tr 'A-Z ' 'a-z-'`"
    STAGE="../staged/$LCNAME"
    mkdir $STAGE &&
    (
        cd $STAGE &&
        cp "../../orig/$d"/*.pdf $LCNAME.pdf &&
        cat >GRADING.txt <<EOF
$@
$NAME


EOF
    )
done

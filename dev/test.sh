#!/usr/bin/env bash

# Usage: test.sh [testname]

trap "echo aborted; exit;" SIGINT SIGTERM

if [ -z "$1" ] ; then
    TESTS=tests/*.vd
else
    TESTS=tests/$1.vd
fi

for i in $TESTS ; do
    echo "--- $i"
    outbase=${i##tests/}
    if [ "${i%-notest.vd}-notest" == "${i%.vd}" ]
    then
        PYTHONPATH=. bin/vd --play $i --batch
    else
        PYTHONPATH=. bin/vd --confirm-overwrite=False --play $i --batch --output tests/golden/${outbase%.vd}.tsv
    fi
done
echo '=== git diffs ==='
git --no-pager diff --exit-code --numstat tests/

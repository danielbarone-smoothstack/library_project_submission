#!/bin/sh

while read line; do
    VALUE=$line   ## No spaces allowed
    python driver.py "$line" "$line" NEW_PARA 5  ## Quote properly to isolate arguments well
    echo "$VALUE+huh"  ## You don't expand without $
done < test_input.txt
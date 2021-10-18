#!/bin/bash

# https://imagemagick.org/script/command-line-options.php

DAYS=3

minutes=1
for day in $(seq -f "%02g" 1 $DAYS); do
    for minute in $(seq -f "%02g" 1 $minutes); do
        TIMESTAMP="202109${day}_13${minute}00"
        COLOR="rgb($(($RANDOM%128 + 128)),$(($RANDOM%128 + 128)),$(($RANDOM%128 + 128)))"

        echo "# $TIMESTAMP"

        LINE="line $(($RANDOM%1024)),$(($RANDOM%768)) $(($RANDOM%1024)),$(($RANDOM%768))"

        convert -size 1024x768 -draw "$LINE" canvas:"$COLOR" -pointsize 70 -fill black -stroke gray -strokewidth 1 -gravity northwest -draw "text 20,20 '$TIMESTAMP-01'" $TIMESTAMP-01.png
        for IDX in {02..12}; do
            convert -size 1024x768 -draw "$LINE" canvas:"$COLOR" -pointsize 70 -fill black -stroke gray -strokewidth 1 -gravity northwest -draw "text 20,20 '$TIMESTAMP-${IDX}'" $TIMESTAMP-${IDX}.png
        done
        ls $TIMESTAMP-*.png
        ffmpeg -y -framerate 4 -i $TIMESTAMP-%02d.png $TIMESTAMP.mp4 > /dev/null 2>&1
        rm $(ls $TIMESTAMP-*.png | grep -v $TIMESTAMP-01.png)
    done
    ((minutes++))
done

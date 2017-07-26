#!/bin/bash

ffmpeg -i $1 -c:v libx264 -profile:v baseline -pix_fmt yuv420p -acodec aac $1.insta.mp4

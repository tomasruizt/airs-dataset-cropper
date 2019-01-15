#!/usr/bin/env bash
source env/bin/activate
python crop_img.py --dataset-dir=$1 --processes=$2 &>out.log
sudo shutdown

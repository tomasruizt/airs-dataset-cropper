#!/usr/bin/env bash
source env/bin/activate
python crop_img.py --dataset-dir=./train --processes=16 &>out.log
sudo shutdown

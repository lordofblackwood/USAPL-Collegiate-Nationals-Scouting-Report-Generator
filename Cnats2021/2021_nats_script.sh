#!/bin/bash
#curl -s -d /dev/null https://docs.google.com/spreadsheets/d/1lyTAwz_9JU-kRDNC_v7I2RpRXIrI1lXoAknRnzkAClU/gviz/tq?tqx=out:csv > cnat_2021.csv
python get_nats_csv.py 
dos2unix cnat_2021.csv 2> /dev/null
python read_nats_csv.py
mv *.xlsx results/

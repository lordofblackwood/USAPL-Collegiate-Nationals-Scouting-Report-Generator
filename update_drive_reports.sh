#!/bin/bash
curl -s -d /dev/null https://docs.google.com/spreadsheets/d/1Ch0l3LlZqS5CAjQLeBbx0oIgs9VIvVtad78QlGkZZGE/export?exportFormat=csv > cnat.csv
dos2unix cnat.csv 2> /dev/null
python read_nats_csv.py
mv Women* ~/Google\ Drive\ File\ Stream/My\ Drive/Women\'s\ Scouting\ reports\ 
mv Men*   ~/Google\ Drive\ File\ Stream/My\ Drive/Scouting\ reports\ because\ Mike\ doesn\'t\ understand\ python\ excel\ libraries

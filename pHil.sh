#!/bin/bash

echo "Welcome to pHil the gap, would you like to use the sensor instrument, please type m. If you want to send your data, please type s. If you want to quit, type q."

while true; do
  read -p "Enter your choice: " choice

  case $choice in
    [Mm]* ) python3 pHil.py; break;;
    [Ss]* ) scp -P 2678 data_log.csv group12@quorkel.com:http/; break;;
    [Qq]* ) exit;;
    * ) echo "Please answer m, s or q.";;
  esac
done


rm *.dat
rm ebay_data.db

python3 ./parser.py ./ebay_data/*.json

sqlite3 ebay_data.db < create.sql
sqlite3 ebay_data.db < load.txt

import csv
from my91test1 import use_thunder_download
import time
with open('info.csv', 'rt+', encoding="utf-8") as f:
	f_csv = csv.reader(f)
	for row in f_csv:
		use_thunder_download(row[1], row[0])
		print(row)
		a = input('skip or continue? enter for skip; certain char for continue:')

import os
import io
from datetime import datetime, date
from datetime import timedelta

# Folder where reports are stored
BASE_DIR = "/Users/Glennon/Documents/erins_reports_test"

# Attempt to make folder if not exist
try:
  os.mkdir(BASE_DIR)
except:
  pass


def make_file(date, duration, animal_name, subject, o_data):
  subject = subject.lower()
  test = True
  if "foil" in subject or "3f" in subject or "reversal" in subject or "bb" in subject or "1313vs" in subject:
    test = False
  if test is True:
    return
  date = date.replace("/", "_")
  file_name = "%s_%s_%s_%s.csv" % (date, duration, animal_name, subject)
  file_name = os.path.join(BASE_DIR, file_name)
  fout = open(file_name, 'w')
  for line in o_data:
    fout.write("%s\n" % "\t".join(line))
  fout.close()


def parse_erin(line_number, filename, data):
  animal_name = data[line_number].split(": ")[-1].strip()
  line_number = line_number - 2
  date = data[line_number].split(' ')[2].strip()
  line_number = line_number + 6
  start = data[line_number].split(": ")[-1].strip()
  start = datetime.strptime(start, '%H:%M:%S').time()
  line_number = line_number + 1
  end = data[line_number].split(": ")[-1].strip()
  end = datetime.strptime(end, '%H:%M:%S').time()
  duration = datetime.combine(datetime(1,1,1,0,0,0), end) - datetime.combine(datetime(1,1,1,0,0,0), start)
  line_number += 1
  subject = data[line_number].replace('MSN: ','').strip()
  while not data[line_number].startswith('O:'):
    line_number += 1
  line_number += 1
  o_data = []
  while not data[line_number].startswith('P:'):
    o_data.append(data[line_number].strip().split()[1:])
    line_number += 1
  make_file(date, duration, animal_name, subject, o_data)

def parse_file(f):
  print(f)
  data = open(f).readlines()
  for i, line in enumerate(data):
    if "_EG" in line:
        parse_erin(i, f, data)



fs = os.listdir('./')
for f in fs:
  if f != ".DS_Store":
    parse_file(f)

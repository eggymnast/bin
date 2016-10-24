import os

# Folder where reports are stored
BASE_DIR = "/Users/Glennon/Documents/erins_reports"

# Attempt to make folder if not exist
try:
  os.mkdir(BASE_DIR)
except:
  pass


def make_file(date, animal_name, subject, o_data):
  subject = subject.lower()
  test = True
  if "foil" in subject or "3f" in subject or "reversal" in subject or "bb" in subject:
    test = False
  if test is True:
    return
  date = date.replace("/", "_")
  file_name = "%s_%s_%s.csv" % (date, animal_name, subject)
  file_name = os.path.join(BASE_DIR, file_name)
  fout = open(file_name, 'w')
  for line in o_data:
    fout.write("%s\n" % "\t".join(line))
  fout.close()


def parse_erin(line_number, filename, data):
  animal_name = data[line_number].split(": ")[-1].strip()
  line_number = line_number - 2
  date = data[line_number].split(' ')[2].strip()
  line_number += 8
  subject = data[line_number].replace('MSN: ','').strip()
  while not data[line_number].startswith('O:'):
    line_number += 1
  line_number += 1
  o_data = []
  while not data[line_number].startswith('P:'):
    o_data.append(data[line_number].strip().split()[1:])
    line_number += 1
  make_file(date, animal_name, subject, o_data)

def parse_file(f):
  data = open(f).readlines()
  for i, line in enumerate(data):
    if "_EG" in line:
        parse_erin(i, f, data)



fs = os.listdir('./')
for f in fs:
  parse_file(f)

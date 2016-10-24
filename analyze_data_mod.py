from __future__ import division
from os import listdir
from os.path import isfile
from scipy.stats import norm
import datetime
from datetime import date
import os
import pandas as pandas
import re
import sys




def get_data_from_file(filename):
    """
    You wrote this!  Good Job!
    We changed it to have a "return" instead of a "side effect" of printing
    Args:
        filename (string): absolute or local path to a file with csv data
    Returns:
        dict: All the needed information from aggregating the csv data
    """
    data = open(filename).readlines()
    data = [[float(y) for y in x.split()] for x in data]
    df = pandas.DataFrame(data)

    #names = df.columns.values
    #print names
    def freq_resp(freq):

        freqfalse = len(df[(df[0] == freq) & (df[3]==3.0)])
        freqwithold = len(df[(df[0] == freq) & (df[3]==4.0)])
        freqhit = len(df[(df[0] == freq) & (df[3]==1.0)])
        freqmiss = len(df[(df[0] == freq) & (df[3]==2.0)])

        divisor = freqwithold + freqmiss + freqfalse + freqhit
        if divisor == 0:
            divisor = divisor + 1

        freq_resp = (freqhit + freqfalse) / (divisor) * 100

        return freq_resp


    fivehund = freq_resp(500)
    onethous = freq_resp(1000)
    twothous = freq_resp(2000)
    fourthous = freq_resp(4000)
    eightthous = freq_resp(8000)
    sixteenthous = freq_resp(16000)
    thirtytwothous = freq_resp(32000)


    response = df[:][3]

    hit = sum(1 for item in response if item == (1.0))
    if hit is 0:
        hit = hit + 1
    miss = sum(1 for item in response if item == (2.0))
    if miss is 0:
        miss = miss + 1
        #print("miss was zero")
    false = sum(1 for item in response if item == (3.0))
    if false is 0:
        false = false + 1
        #print("false was zero")
    withold = sum(1 for item in response if item == (4.0))

    trials = hit + miss + false + withold

    hit_rate = (hit / (hit + miss) * 100)
    false_positive_rate = (false / (false + withold) * 100)

    d1 = norm.ppf(hit_rate/100)
    d2 = norm.ppf(false_positive_rate/100)

    dprime = d1 - d2

    precision = hit / (hit + false)
    recall = hit / (hit + miss)
    denominator = precision + recall

    if denominator==0:
        F_score = "N/A"
    else:
        F_score = (2 * precision * recall) / (denominator)

    ##dur = [data_dictionary['duration'] for duration in data_dictionary]

    return {
        "hit": hit,
        "miss": miss,
        "false": false,
        "withold": withold,
        "trials": trials,
        "hit_rate": hit_rate,
        "false_positive_rate": false_positive_rate,
        "dprime": dprime,
        "precision": precision,
        "recall": recall,
        "F_score": F_score,
        "500 Hz": fivehund,
        "1000 Hz": onethous,
        "2000 Hz": twothous,
        "4000 Hz": fourthous,
        "8000 Hz": eightthous,
        "16000 Hz": sixteenthous,
        "32000 Hz": thirtytwothous
    }


def parse_filename(filename):
    """
    I wrote this one for you.  It uses a tool called regular expressions
    https://en.wikipedia.org/wiki/Regular_expression
    Basically pattern matching on a String to pull out parts you care about
    Args:
        filename (string): absolute or local path to a file with csv data
    Returns:
        dict: All the needed information from parsing the filename
    """
    PATTERN = r"(?P<date>\d\d_\d\d_\d\d)_(?P<duration>\d:\d\d:\d\d)_(?P<animal>.*?)_(?P<program>.+).csv"
    filename = os.path.basename(filename)
    m = re.match(PATTERN, filename)
    d = m.groupdict()


    # We want the date to be a date object so we can sort it nicely :)
    d['date'] = datetime.datetime.strptime(d['date'], "%m_%d_%y")
    def get_min(time_str):
        h, m, s = time_str.split(':')
        return int(h) * 60 + int(m) + int(s) / 60

    d['duration'] = get_min(d['duration'])



#def get_sec(time_str):
#    h, m, s = time_str.split(':')
#    return int(h) * 3600 + int(m) * 60 + int(s)


    return d


def append_row(dataframe, data_dictionary):
    """
    TODO(ERIN)
    Args:
        dataframe (DataFrame): DataFrame with all animal data up to now
        data_dictionary (Dict): Dictionary with new data to append to Dataframe
    Returns:
        DataFrame: A new Dataframe with data_dictionary appended
    """
    updated = dataframe.append(data_dictionary, ignore_index=True)
    return updated


def save_to_file(out_folder, animal_name, dataframe):
    """
    TODO(ERIN)
    Time to save our results!
    This function has the Side Effect of creating a file in
    <out_folder>/<animal_name>.csv with the contents of dataframe

    Args:
        out_folder (String): folder which we want to save our data to
        animal_name (String): Name of the animal who this data is on
        dataframe (DataFrame): DataFrame containing all the data
    Returns:
        None:


karl tip: change column order in dataframe to change order; reorder dataframe columns (google)

    """
    file_name = "%s.xls" % (animal_name)
    file_name = os.path.join(out_folder, file_name)


    cols = dataframe.columns.tolist()
    #print ('original:', cols)

    #neworder=[11, 0, 17, 19, 15, 18, 21, 5, 4, 20, 3, 16, 1, 12, 7, 14, 6, 8, 2, 10, 9, 13]
    #cols = [cols[i] for i in neworder]
    #print ('reorderd:', cols)
    #neworder = [[]]
    neworder = ['date','animal','program','duration','trials','hit','miss','false','withold','hit_rate','false_positive_rate','dprime','recall','precision','F_score','500 Hz', '1000 Hz','2000 Hz','4000 Hz', '8000 Hz', '16000 Hz', '32000 Hz']

    #cols = list(neworder.columns.values)
    dataframe = dataframe[neworder]



# df = df[['f','f']]
# cols = list(df.columns.values)


    dataframe.to_csv(file_name, sep='\t', index=False)
    return



def get_all_data_as_dict(filename):
    """
    TODO(ERIN)
    This function aggegates all the data from a single file
    It should call "parse_filename" and "get_data_from_file"
    and join the results into a single dictionary
    Args:
        filename (String): filename which we want to get data on
    Returns:
        dict: Dictionary with all data from parse_filename and
              get_data_from_file
    """
    filedata = parse_filename(filename)
    data = get_data_from_file(filename)
    data_dictionary = filedata.copy()
    data_dictionary.update(data)
    return data_dictionary


def get_all_files_in_folder(folder):
    """
    TODO(ERIN)
    Returns a List of Strings which contain every filename in a folder
    Args:
        folder (String): Folder Path which we want files in
    Returns:
        list<String>: List of filenames in folder
    """
    folder = os.listdir(folder)
    while ".DS_Store" in folder:
        folder.remove(".DS_Store")
    return folder


def main(in_folder, out_folder):
    files = get_all_files_in_folder(in_folder)
    dataframes = {}
    for f in files:
        f = os.path.join(in_folder, f)
        d = get_all_data_as_dict(f)
        if d['animal'] not in dataframes:
            dataframes[d['animal']] = pandas.DataFrame([], columns=d.keys())
        df = append_row(dataframes[d['animal']], d)
        dataframes[d['animal']] = df

    for animal_name, df in dataframes.items():
        save_to_file(out_folder, animal_name, df)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("python analyze.py <csv_input_folder> <output_folder>")
        sys.exit(1)

        # Folder where reports are stored
        #BASE_DIR = "/Users/Glennon/Documents/erins_data"

        # Attempt to make folder if not exist
        #try:
         # os.mkdir(BASE_DIR)
        #except:
        #  pass

    main(sys.argv[1], sys.argv[2])

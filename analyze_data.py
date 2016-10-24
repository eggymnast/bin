from __future__ import division
import sys

def main(filename):
    data = open(filename).readlines()
    data = [[float(y) for y in x.split()] for x in data]
    ##print data


    import numpy as np
    ##myarray = np.array(data)

    import pandas as pandas
    from scipy.stats import norm

    df = pandas.DataFrame(data)

    ##print df

    #df.columns = ['Frequency','Col_B','Col_C','Response']
    #byresponse = df.groupby('Response')
    #values = byresponse.count()

    response = df[:][3]

    hit=sum(1 for item in response if item==(1.0))
    miss=sum(1 for item in response if item==(2.0))
    if miss is 0:
        miss = miss + 1
        print "miss was zero"
    false=sum(1 for item in response if item==(3.0))
    if false is 0:
        false = false + 1
        print "false was zero"
    withold=sum(1 for item in response if item==(4.0))

    print "hit = %s" % hit
    print "miss = %s" % miss
    print "false = %s" % false
    print "withold = %s" % withold

    detection = (hit / (hit + miss) * 100)
    discrimination = (false / (false + withold) * 100)
    print "detection = %s" % detection
    print "discrimination = %s" % discrimination

    d1 = norm.ppf(detection/100)
    d2 = norm.ppf(discrimination/100)

    dprime = d1 - d2
    print "d' = %s" % dprime

if __name__ == "__main__":
    main(sys.argv[1])

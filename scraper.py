import sys
if sys.version_info >= (3,0,0):
    is3 = True
    from urllib import request
else:
    is3 = False
    import urllib2
from bs4 import BeautifulSoup
import csv
from time import strftime
import os
import subprocess
import time

def processtable(url):
    props = []
    data = []
    yesno = []
    if(is3):
        html = request.urlopen(url)
    else:
        html = urllib2.urlopen(url)
    soup = BeautifulSoup(html)
    table = soup.find_all('table', id='ctl00_CountySummary_tblCountySummary')[0]
    trs = table.find_all('tr')
    for i in range(0,len(trs)):
        tds = trs[i].find_all('td')
        if i == 0:
            for i in range(0,len(tds)):
                if not i == 0:
                    props.append(tds[i]['title'])
                    props.append('')
        elif i == 1:
            for i in range(0,len(tds)):
                yesno.append(tds[i].find(text=True))
        else:
            row = []
            for i in range(0,len(tds)):
                row.append(tds[i].find(text=True).replace(',','').strip())
            data.append(row)
    return props,yesno,data

def writedata(props,yesno,data,outfile):
    if(is3):
        c = csv.writer(open(outfile, "w", newline=''))
    else:
        c = csv.writer(open(outfile, "wb"))
    c.writerow(props)
    c.writerow(yesno)
    for row in data:
        c.writerow(row)

def gitpush(outfile):
    isodatetime = strftime("%Y-%m-%d %H:%M:%S")
    cmd = 'git add %s; git commit -m "%s"' % (outfile, isodatetime)
    pipe = subprocess.Popen(cmd, shell=True, cwd=os.getcwd())
    pipe.wait()

def main():
    url = "http://nyenr.elections.state.ny.us/UnofficialElectionResultsCounty.aspx"
    outfile = "propositions.csv"

    i = 0
    while True:
        print("Running scrape #{0}".format(i))
        print("Reading Table from Web ...")
        props,yesno,data = processtable(url)
        print ("Writing out CSV ..")
        writedata(props,yesno,data,outfile)
        print ("Pushing to Github ...")
        gitpush(outfile)
        print ("Waiting 60 seconds ...")
        time.sleep(60)
        i += 1

main()


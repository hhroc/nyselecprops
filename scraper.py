import urllib2
from bs4 import BeautifulSoup
import csv

def processtable(url):
    props = []
    data = []
    yesno = []
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
        elif i == 1:
            for i in range(0,len(tds)):
                yesno.append(tds[i].find(text=True))
        else:
            row = []
            for i in range(0,len(tds)):
                row.append(tds[i].find(text=True))
            data.append(row)
    return props,yesno,data

def writedata(props,yesno,data,outfile):
    c = csv.writer(open(outfile, "wb"))
    c.writerow(props)
    c.writerow(yesno)
    for row in data:
        c.writerow(row)

def gitpush(outfile):
    # zomg pill request me
    return

def main():
    url = "http://nyenr.elections.state.ny.us/UnofficialElectionResultsCounty.aspx"
    outfile = "propositions.csv"
    print "Reading Table from Web ..."
    props,yesno,data = processtable(url)
    print "Writing out CSV .."
    writedata(props,yesno,data,outfile)
    print "Pushing to Github ..."
    gitpush(outfile)
    print "Done."

main()

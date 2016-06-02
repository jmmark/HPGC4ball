import mechanize
from bs4 import BeautifulSoup
import re
import csv

#myGhin = "8474820"

#function to scrape the index from the ghin server
def indexFinder(theGhin):
    url = ("http://widgets.ghin.com/HandicapLookupResults.aspx?entry=1&dynamic=&small=0&"
        "css=Default&ghinno=%s&hidename=0&showmsg=0&showheader=1&showtabheader=0&combine"
        "hieff=0&showheadertext=1&showfootertext=1&tab=0") %(theGhin,)
    br = mechanize.Browser()
    br.set_handle_robots(False)
    results = br.open(url)
    content = results.read()
    mySoup = BeautifulSoup(content,"html.parser")
    myIdx = mySoup("td",{"class":"ClubGridHandicapIndex"})
    myEffDt = mySoup("td",{"class":"ClubGridEffectiveDate"})
    theIndex = myIdx[0].string
    theDate = myEffDt[0].string
    return (theIndex.strip(),theDate.strip())

#get the list of GHINs from the roster
with open("currentRoster.csv","r") as csvfile:
    roster = csv.DictReader(csvfile)
    ghinList = []
    for row in roster:
        curGhin = str(row["ghin"])
        if len(curGhin) < 7:
            fronter = "0" * (7 - len(curGhin))
            curGhin = fronter + curGhin
        ghinList.append(curGhin)

#loop through each GHIN, write the results if available
fieldnames = ["ghin","index","asOf"]
with open("indexResults.csv","w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    i = 0
    for ghin in ghinList:
        i = i + 1
        print i
        try:
            res = indexFinder(ghin)
            writer.writerow({"ghin":ghin,"index":res[0],"asOf":res[1]})
        except:
            writer.writerow({"ghin":ghin,"index":"err","asOf":"err"})

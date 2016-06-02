import mechanize
from bs4 import BeautifulSoup
import re
import csv

#myGhin = "8474820"
class GHINS(object):
    htmlGhin = []
    htmlIdx = []
    htmlEffDt = []
    def __init__(self,bigGhin):
        url = ("http://widgets.ghin.com/HandicapLookup.aspx?entry=1&"
            "ghinno=%s&css=default&dynamic=&small=0"
            "&showheader=1&showheadertext=1&showfootertext=1&tab=2") %(bigGhin,)
        br = mechanize.Browser()
        br.set_handle_robots(False)
        results = br.open(url)
        content = results.read()
        mySoup = BeautifulSoup(content,"html.parser")
        self.htmlGhin = mySoup("span",{"id":re.compile("lblGHIN$")})
        self.htmlIdx = mySoup("span",{"id":re.compile("lblHI$")})
        self.htmlEffDt = mySoup("span",{"id":re.compile("lblEffdt$")})


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

bigGhin = ",".join(ghinList)

tryMe = GHINS(bigGhin)




#print htmlGhin
#myIdx = mySoup("td",{"class":"ClubGridHandicapIndex"})
#myEffDt = mySoup("td",{"class":"ClubGridEffectiveDate"})
#theIndex = myIdx[0].string
#theDate = myEffDt[0].string
#return (theIndex.strip(),theDate.strip())



#loop through each GHIN, write the results if available
fieldnames = ["ghin","index","asOf"]
with open("indexResults.csv","wb") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()

    for k in range(0,len(ghinList)/10+1):
        maxInd = min((k*10)+10,len(ghinList)) 
        print k,maxInd
        bigGhin = ",".join(ghinList[k*10:maxInd])
        print bigGhin
        tryMe = GHINS(bigGhin)
        for i in range(0,len(tryMe.htmlGhin)):

            writer.writerow({"ghin":tryMe.htmlGhin[i].string.strip(),
                "index":tryMe.htmlIdx[i].string.strip(),
                "asOf":tryMe.htmlEffDt[i].string.strip()})
#    for ghin in ghinList:
#        i = i + 1
#        print i
#        try:
#            res = indexFinder(ghin)
#            writer.writerow({"ghin":ghin,"index":res[0],"asOf":res[1]})
#        except:
#            writer.writerow({"ghin":ghin,"index":"err","asOf":"err"})

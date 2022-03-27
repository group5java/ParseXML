import requests
import xml.etree.ElementTree as ET
import xml.etree.ElementTree as Xet
import pandas as pd
from xml.etree import ElementTree
import csv
import datetime

yearToParse = input("Please input 'all' to parse the whole data or any specific year: ")
today = datetime.date.today()
if(yearToParse == 'all'):
    startYear = 2018
    endYear = today.year + 1
else:
    startYear = int(yearToParse)
    endYear = int(yearToParse) + 1

# CREATE CSV FILE
csvfile_1 = open("alert_list.csv",'w', encoding='utf8', newline="")
csvfile_writer_1 = csv.writer(csvfile_1)

# ADD THE HEADER TO CSV FILE
csvfile_writer_1.writerow(["title", "id", "title-item","id-item", "link-item", "cpe-item", "cve-item", "published-item", "updated-item"])

# Get XML from API
for year in range (startYear, endYear):
    pathApi = "https://jvndb.jvn.jp/myjvn?method=getAlertList&feed=hnd&datePublished=" + str(year)
    response = requests.get(pathApi)
    root = ET.fromstring(response.text)
    tree = ET.ElementTree(root)
    tree.write("data_alert.xml")
    print('Get API to XML in ' + str(year) + ' successfully')

    fixedFile = open("data_alert_fixed.xml",'w', encoding='utf8')
    with open('data_alert.xml') as file:
        for line in file:
                line = line.replace("ns0:", "")
                line = line.replace("ns1:", "")
                line = line.replace("ns2:", "")
                line = line.replace("ns3:", "")
                line = line.replace("ns4:", "")
                line = line.replace("ns5:", "")
                fixedFile.write(line)

    fixedFile.close()

    # Parsing XML to CSV
    xml = ElementTree.parse("data_alert_fixed.xml")
    root = xml.getroot()

    for object in root.findall("./entry"):
        currentTitle = object.find("title").text
        currentId = object.find("id").text
        
        for item in object.findall("./items/item"):
            currentTitleItem = item.find("title").text
            currentIdItem = item.find("identifier").text
            currentLinkItem = item.find("link").attrib['href']

            if(str(item.find("cpe")) != 'None'):
                currentCpeItem = item.find("cpe").text
            else: 
                currentCpeItem = "-"

            if(currentTitleItem.find("CVE") != -1):
                if(len(currentTitleItem) - currentTitleItem.find("CVE") <=13):
                    currentCveItem = currentTitleItem[currentTitleItem.find("CVE"):]
                else:
                    tempCve = currentTitleItem[currentTitleItem.find("CVE") + 13]
                    if(tempCve.isnumeric()):
                        currentCveItem = currentTitleItem[currentTitleItem.find("CVE"):currentTitleItem.find("CVE")+14]
                    else:
                        currentCveItem = currentTitleItem[currentTitleItem.find("CVE"):currentTitleItem.find("CVE")+13]
            else:
                currentCveItem = "-"
                
            currentPublishedItem = item.find("published").text
            currentUpdatedItem = item.find("updated").text

            currentCsvLine = [currentTitle, currentId, currentTitleItem, currentIdItem, currentLinkItem, currentCpeItem, currentCveItem, currentPublishedItem, currentUpdatedItem]
            csvfile_writer_1.writerow(currentCsvLine)

    print('csv parsed in ' + str(year) + ' successfully')


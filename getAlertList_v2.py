import requests
import xml.etree.ElementTree as ET
import xml.etree.ElementTree as Xet
import pandas as pd
from xml.etree import ElementTree
import csv

# Get XML from API
response = requests.get("https://jvndb.jvn.jp/myjvn?method=getAlertList&feed=hnd")
root = ET.fromstring(response.text)
tree = ET.ElementTree(root)
tree.write("data_alert.xml")
print('Get API to XML successfully')

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
# CREATE CSV FILE
csvfile_1 = open("alert_list.csv",'w', encoding='utf8', newline="")
csvfile_writer_1 = csv.writer(csvfile_1)

# ADD THE HEADER TO CSV FILE
csvfile_writer_1.writerow(["title", "id", "title-item","id-item", "link-item", "cpe-item", "published-item", "updated-item"])

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
        print(str(item.find("cpe")))
        if(str(item.find("cpe")) != 'None'):
            currentCpeItem = item.find("cpe").text
        else: 
            currentCpeItem = "-"

        currentPublishedItem = item.find("published").text
        currentUpdatedItem = item.find("updated").text

        currentCsvLine = [currentTitle, currentId, currentTitleItem, currentIdItem, currentLinkItem, currentCpeItem, currentPublishedItem, currentUpdatedItem]
        csvfile_writer_1.writerow(currentCsvLine)

print('csv parsed successfully')


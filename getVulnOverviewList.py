import requests
import xml.etree.ElementTree as ET
import xml.etree.ElementTree as Xet
import pandas as pd
from xml.etree import ElementTree
import csv

# Get XML from API
response = requests.get("https://jvndb.jvn.jp/myjvn?method=getVulnOverviewList&feed=hnd")
root = ET.fromstring(response.text)
tree = ET.ElementTree(root)
tree.write("data_vuln_overview.xml")
print('Get API to XML successfully')
fixedFile = open("data_vuln_overview_fixed.xml",'w', encoding='utf8')
with open('data_vuln_overview.xml') as file:
    for line in file:
            line = line.replace("ns0:", "")
            line = line.replace("ns1:", "")
            line = line.replace("ns2:", "")
            line = line.replace("ns3:", "")
            line = line.replace("ns4:", "")
            line = line.replace("ns5:", "")
            line = line.replace("dc:", "")
            fixedFile.write(line)

fixedFile.close()
# CREATE CSV FILE
csvfile_1 = open("vuln_overview_list.csv",'w', encoding='utf8', newline="")
csvfile_writer_1 = csv.writer(csvfile_1)

# ADD THE HEADER TO CSV FILE
csvfile_writer_1.writerow(["title","link","description", "creator", "identifier", "cpe", "date", "issued", "modified"])

# Parsing XML to CSV
xml = ElementTree.parse("data_vuln_overview_fixed.xml")
root = xml.getroot()

titleArray=[]
linkArray = []
descriptionArray = []
creatorArray=[]
identifierArray = []
cpeArray = []
dateArray=[]
issuedArray = []
modifiedArray = []

title = root.findall("./item/title")
link = root.findall("./item/link")
description = root.findall("./item/description")
creator = root.findall("./item/creator")
identifier = root.findall("./item/identifier")
cpe = root.findall("./item/cpe")
date = root.findall("./item/date")
issued = root.findall("./item/issued")
modified = root.findall("./item/modified")


for object in title :
      titleArray.append(object.text)
for object in link :
      linkArray.append(object.text)
for object in description :
      descriptionArray.append(object.text)
for object in creator :
      creatorArray.append(object.text)
for object in identifier :
      identifierArray.append(object.text)
for object in cpe :
      cpeArray.append(object.text)   
for object in date :
      dateArray.append(object.text)
for object in issued :
      issuedArray.append(object.text)
for object in modified :
      modifiedArray.append(object.text)   

for i in range(len(title)):
      csv_line = [titleArray[i], linkArray[i], descriptionArray[i], creatorArray[i], identifierArray[i], cpeArray[i], dateArray[i], issuedArray[i], modifiedArray[i]]
      csvfile_writer_1.writerow(csv_line)


print('csv file exported successfully')
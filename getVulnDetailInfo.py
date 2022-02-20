import requests
import xml.etree.ElementTree as ET
import xml.etree.ElementTree as Xet
import pandas as pd
from xml.etree import ElementTree
import csv

# Get XML from API
response = requests.get("https://jvndb.jvn.jp/myjvn?method=getVulnDetailInfo&feed=hnd")
root = ET.fromstring(response.text)
tree = ET.ElementTree(root)
tree.write("data_vuln_detail.xml")
print('Get API to XML successfully')
fixedFile = open("data_vuln_detail_fixed.xml",'w', encoding='utf8')
with open('data_vuln_detail.xml') as file:
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
csvfile_1 = open("vuln_detail_list.csv",'w', encoding='utf8', newline="")
csvfile_writer_1 = csv.writer(csvfile_1)

# ADD THE HEADER TO CSV FILE
csvfile_writer_1.writerow(["version","method","lang", "retCd", "errCd", "errMsg"])

# Parsing XML to CSV
xml = ElementTree.parse("data_vuln_detail_fixed.xml")
root = xml.getroot()

versionArray = []
methodArray = []
langArray = []
retCdArray = []
errCdArray = []
errMsgArray = []

item = root.findall("./Status")


for object in item :
      versionArray.append(object.attrib['version'])
      methodArray.append(object.attrib['method'])
      langArray.append(object.attrib['lang'])
      retCdArray.append(object.attrib['retCd'])
      errCdArray.append(object.attrib['errCd'])
      errMsgArray.append(object.attrib['errMsg'])

  

for i in range(len(item)):
      csv_line = [versionArray[i], methodArray[i], langArray[i], retCdArray[i], errCdArray[i], errMsgArray[i]]
      csvfile_writer_1.writerow(csv_line)


print('csv file exported successfully')
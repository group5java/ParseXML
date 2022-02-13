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
tree.write("data.xml")
print('Get API to XML successfully')

fixedFile = open("data_fixed.xml",'w', encoding='utf8')
with open('data.xml') as file:
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
csvfile_writer_1.writerow(["title","id","published","updated"])

# Parsing XML to CSV
xml = ElementTree.parse("data_fixed.xml")
root = xml.getroot()

titleArray=[]
idArray = []
publishedArray = []
updatedArray = []

titleItemArray=[]
idItemArray = []
linkItemArray = []
cpeItemArray = []
publishedItemArray = []
updatedItemArray = []

title = root.findall("./entry/title")
id = root.findall("./entry/id")
published = root.findall("./entry/published")
updated = root.findall("./entry/updated")

titleItem = root.findall("./entry/items/item/title")
idItem = root.findall("./entry/items/item/identifier")
linkItem = root.findall("./entry/items/item/link")
cpeItem = root.findall("./entry/items/item/cpe")
publishedItem = root.findall("./entry/items/item/published")
updatedItem = root.findall("./entry/items/item/updated")

for object in title :
      titleArray.append(object.text)
for object in id :
      idArray.append(object.text)
for object in published :
      publishedArray.append(object.text)   
for object in updated :
      updatedArray.append(object.text)

for object in titleItem :
      titleItemArray.append(object.text)
for object in idItem :
      idItemArray.append(object.text)
for object in linkItem :
      linkItemArray.append(object.attrib['href'])
for object in cpeItem:
      cpeItemArray.append(object.text)
for object in publishedItem :
      publishedItemArray.append(object.text)
for object in updatedItem :
      updatedItemArray.append(object.text)

for i in range(len(title)):
      csv_line = [titleArray[i], idArray[i], publishedArray[i], updatedArray[i]]
      csvfile_writer_1.writerow(csv_line)

print(len(linkItemArray))
csvfile_1.close()

csvfile_2 = open("alert_list_item.csv",'w', encoding='utf8', newline="")
csvfile_writer_2 = csv.writer(csvfile_2)

csvfile_writer_2.writerow(["title","identifier","link","published", "updated"])

for i in range(len(titleItem)):
      csv_line = [titleItemArray[i], idItemArray[i], linkItemArray[i], publishedItemArray[i], updatedItemArray[i]]
      csvfile_writer_2.writerow(csv_line)

print('csv file exported successfully')
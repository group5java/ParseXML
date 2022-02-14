import requests
import xml.etree.ElementTree as ET
import xml.etree.ElementTree as Xet
import pandas as pd
from xml.etree import ElementTree
import csv

# Get XML from API
response = requests.get("https://jvndb.jvn.jp/myjvn?method=getProductList&feed=hnd")
root = ET.fromstring(response.text)
tree = ET.ElementTree(root)
tree.write("data_product.xml")
print('Get API to XML successfully')
fixedFile = open("data_product_fixed.xml",'w', encoding='utf8')
with open('data_product.xml') as file:
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
csvfile_1 = open("vendor_list.csv",'w', encoding='utf8', newline="")
csvfile_writer_1 = csv.writer(csvfile_1)

# ADD THE HEADER TO CSV FILE
csvfile_writer_1.writerow(["vendor","cpe","vid"])

# Parsing XML to CSV
xml = ElementTree.parse("data_product_fixed.xml")
root = xml.getroot()

vendorArray=[]
cpeArray = []
vidArray = []

vendor = root.findall("./VendorInfo/Vendor")

productArray=[]
cpeProductArray = []
pidArray = []

product = root.findall("./VendorInfo/Vendor/Product")

for object in vendor :
      vendorArray.append(object.attrib['vname'])
for object in vendor :
      cpeArray.append(object.attrib['cpe'])
for object in vendor :
      vidArray.append(object.attrib['vid'])   

for object in product :
      productArray.append(object.attrib['pname'])
for object in product :
      cpeProductArray.append(object.attrib['cpe'])
for object in product :
      pidArray.append(object.attrib['pid'])

for i in range(len(vendor)):
      csv_line = [vendorArray[i], cpeArray[i], vidArray[i]]
      csvfile_writer_1.writerow(csv_line)

csvfile_1.close()

csvfile_2 = open("product_list.csv",'w', encoding='utf8', newline="")
csvfile_writer_2 = csv.writer(csvfile_2)

csvfile_writer_2.writerow(["product","cpe","vid"])

for i in range(len(product)):
      csv_line = [productArray[i], cpeProductArray[i], pidArray[i]]
      csvfile_writer_2.writerow(csv_line)

print('csv file exported successfully')
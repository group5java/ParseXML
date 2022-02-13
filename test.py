import requests
import csv

r = requests.get('http://jisho.org/api/v1/search/words?keyword=%23common')
data = r.json()

with open('common_words.csv', 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['word','reading'])
    for entry in data["data"]:
        word = entry["japanese"][0]["word"]
        reading = entry["japanese"][0]["reading"]
        writer.writerow({'word':word,'reading':reading,})
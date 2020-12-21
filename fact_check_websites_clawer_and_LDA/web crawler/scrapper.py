import requests
import json
from bs4 import BeautifulSoup

def dateMap(month) -> str:
    if month == "November":
        return str(11)
    elif month == "October":
        return str(10) 
    elif month == "September":
        return str(9) 
    elif month == "August":
        return str(8) 
    elif month == "July":
        return str(7) 
    elif month == "June":
        return str(6) 
    elif month == "May":
        return str(5) 
    elif month == "April":
        return str(4)
    elif month == "March":
        return str(3)
    elif month == "February":
        return str(2)
    elif month == "January":
        return str(1)
    elif month == "December":
        return str(12)
    return "unknown"     

result = []
# w.write("text,result\n")
for page in range(1, 136):
    url = "https://www.politifact.com/search/factcheck/?page=" + str(page) + "&q=covid"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    # print(soup)
    mydivs = soup.findAll("div", {"class": "c-textgroup__title"})
    mydates = soup.findAll("div", {"class": "c-textgroup__author"})
    myimgs = soup.findAll("img", {"class": "c-image__original"})
    # for idx, div in enumerate(mydivs):
    #     print(str(idx) + ": " + div.contents[1].contents[0].string.strip())
    # for idx, img in enumerate(myimgs):
    #     print(str(idx) + ": " + str("true" in img["src"]))
    for i in range(len(mydivs)):
        dic = {}
        dic["context"] = mydivs[i].contents[1].contents[0].string.strip()
        dic["label"] = str("true" in myimgs[i]["src"])
        dateList = mydates[i].text.strip().split(" ")
        dic["date"] = dateList[-3] + '_' + dateMap(dateList[-5]) + '_' + dateList[-4][:-1]
        result.append(dic)
    # for date in mydates:
    #     dateList = date.text.strip().split(" ")
    #     date = dateList[-3] + '_' + dateMap(dateList[-5]) + '_' + dateList[-4][:-1]
    #     print(date)
#     for pair in zip(mydivs, myimgs):
#         w.write(str("true" in pair[1]["src"]) + ',' + pair[0].contents[1].contents[0].string.strip())
#         w.write("\n")
    print("Complete {}/135 pages".format(page))


with open('label.json', 'w') as outfile:
    json.dump(result, outfile)


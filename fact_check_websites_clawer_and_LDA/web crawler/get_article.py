import requests
import json
from bs4 import BeautifulSoup

# w = open("test2.txt", "w")

def dateMap(month) -> str:
    if month == "nov":
        return str(11)
    elif month == "oct":
        return str(10) 
    elif month == "sep":
        return str(9) 
    elif month == "aug":
        return str(8) 
    elif month == "jul":
        return str(7) 
    elif month == "jun":
        return str(6) 
    elif month == "may":
        return str(5) 
    elif month == "apr":
        return str(4)
    elif month == "mar":
        return str(3)
    elif month == "feb":
        return str(2)
    elif month == "jan":
        return str(1)
    elif month == "dec":
        return str(12)
    return "unknown"     
result = {}
for page in range(1, 136):
    url = "https://www.politifact.com/search/factcheck/?page=" + str(page) + "&q=covid"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    # print(soup.prettify())

    # print(soup)


    mydivs = soup.findAll("div", {"class": "c-textgroup__title"})
    for div in mydivs:
        component_in_url = div.contents[1]["href"].split("/")
        component_in_url[3] = dateMap(component_in_url[3])
        key = "_".join(component_in_url[2:5]) + "_" + component_in_url[-2]
        date = "_".join(component_in_url[2:5])
        urlArticle = "https://www.politifact.com" + div.contents[1]["href"]
        reqArticle = requests.get(urlArticle)
        soupArticle = BeautifulSoup(reqArticle.content, "html.parser")
        contextArticle = soupArticle.find("article", {"class": "m-textblock"})
        all_p = contextArticle.contents[1].find_all("p")
        context = ""
        for p in all_p:
            context += str(p.text)
            # file.write(p.text)
        result[key] =  {}
        result[key]["date"] = date
        result[key]["context"] = context

    print("Complete {}/135 pages".format(page))

with open('context2.json', 'w') as outfile:
    json.dump(result, outfile)

# mydivs = soup.find("div", {"class": "c-textgroup__title"})
# print(mydivs.contents[1]["href"].split("/"))

# urlArticle = "https://www.politifact.com" + mydivs.contents[1]["href"]
# print(urlArticle)
# reqArticle = requests.get(urlArticle)
# soupArticle = BeautifulSoup(reqArticle.content, "html.parser")
# a = soupArticle.find("article", {"class": "m-textblock"})
# allP = a.contents[1].find_all("p")
# for p in allP:
#     print(p.text)
# print(type(soupArticle))
# w.write(soupArticle.prettify())

# myimgs = soup.findAll("img", {"class": "c-image__original"})
# for idx, div in enumerate(mydivs):
#     print(str(idx) + ": " + div.contents[1].contents[0].string.strip())
# for idx, img in enumerate(myimgs):
#     print(str(idx) + ": " + str("true" in img["src"]))

# w.close()


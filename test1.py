from bs4 import BeautifulSoup
import requests

results = 100
result_per_page = []
while results > 30:
    result_per_page.append(30)
    results -= 30
result_per_page.append(results)
print(result_per_page)
page = 1
page1 = 0
news_dict = {}
while(True):
    if page == len(result_per_page):
        break
    url = "https://news.ycombinator.com/news?p={page}"
    r = requests.get(url)
    z = BeautifulSoup(r.text, 'lxml')
    news_score = z.find_all("tr", class_ = "athing")

    for i in range(result_per_page[page - 1]):
        j = news_score[i]['id'] # id value
        score = f"score_{j}"
        comments = f"item?id={j}"
        k1 = news_score[i].find("span", class_ = "rank").text[:-1] # news rank
        k2 = news_score[i].find("a", class_ = "titlelink").text # news title
        try:
            k3 = z.find(id = score).text # Score by id
            k3 = int(k3.split(" ")[0])
        except AttributeError:
            k3 = 0
        k41 = z.find_all(href = comments) 
        try:
            k4 = int(k41[0].text.split(" ")[0]) # Time Posted
        except ValueError:
            k4 = 0

        try:
            k5 = int(k41[-1].text[:-9]) # Comment number
        except ValueError:
            k5 = 0
        news_dict[j] = [k1, k2, k3, k4, k5]
        page1 += 1
    page += 1
print(news_dict)
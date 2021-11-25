from bs4 import BeautifulSoup
import requests


sort_by_points = False
sort_by_comment = False
sort_by_default = False

news_dict = {}
results = 32
result_per_page = []
while results > 30:
    result_per_page.append(30)
    results -= 30
result_per_page.append(results)
    
page = 1
page1 = 0
while(page != len(result_per_page) + 1):
    url = f"https://news.ycombinator.com/news?p={page}"
    r = requests.get(url)
    html = r.content
    z = BeautifulSoup(html, 'lxml')
    news_score = z.find_all("tr", class_ = "athing")
    news_subtext = z.find_all("td", class_ = "subtext")
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
        k6 = news_subtext[i].find("span", class_ = "age")["title"]
        news_dict[j] = [k1, k2, k3, k4, k5, k6]
        page1 += 1
    page += 1
print(news_dict)

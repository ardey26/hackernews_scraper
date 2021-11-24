from bs4 import BeautifulSoup
import requests

url = "https://news.ycombinator.com/news"

r = requests.get(url)

z = BeautifulSoup(r.text, 'lxml')

news_score = z.find_all("tr", class_ = "athing")
news_dict = {}
for i in range(len(news_score)):
    j = news_score[i]['id'] # id value
    score = f"score_{j}"
    comments = f"item?id={j}"
    k1 = news_score[i].find("span", class_ = "rank").text[:-1] # news rank
    k2 = news_score[i].find("a", class_ = "titlelink").text # news title
    try:
        k3 = z.find(id = score).text # Score by id
        k4 = z.find_all(href = comments) # Comment by id
        k5 = k4[0].text
        k6 = k4[1].text
        news_dict[j] = [k1, k2, k3, k5, k6]
    except AttributeError:
        news_dict[j] = [k1, k2, "n/a", k5, "n/a"]
        continue
    

for z in news_dict:
    print("Rank:", news_dict[z][0])
    print("Title:", news_dict[z][1])
    print("Points:", news_dict[z][2])
    print("Time:", news_dict[z][3])
    print("Comment #:", news_dict[z][4])
    print("=" * 80)

#result = int(input("How many results would you like to see? "))


        


# with open("hackernews.txt", 'w') as f:
#     for i in range(0, result):
#         f.write(f"Title: {news_title[i].text} \n")
#         f.write(f"Rank:  {news_rank[i].text} \n")
#         f.write("=" * titles)
#         f.write("\n")

# f.close()

from bs4 import BeautifulSoup
import requests

url = "https://news.ycombinator.com/news"
r = requests.get(url)
z = BeautifulSoup(r.text, 'lxml')

sort_by_points = False
sort_by_comment = False

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
choice = int(input("[1] - SORT BY POINTS | [2] - SORT BY COMMENT: "))
if choice == 1:
    sort_by_points = True

elif choice == 2:
    sort_by_comment = True

if(sort_by_points):
    points_sorted_dict = {k: v for k, v in sorted(news_dict.items(), key=lambda item: item[1][2], reverse = True)}
    j = 1
    for i in points_sorted_dict:
        print("Rank:", j)
        print("Title:", points_sorted_dict[i][1])
        print("Points:", points_sorted_dict[i][2])
        print("Time:", points_sorted_dict[i][3])
        print("Comment #:", points_sorted_dict[i][4])
        print("=" * 80)
        j += 1

if(sort_by_comment):
    comments_sorted_dict = {k: v for k, v in sorted(news_dict.items(), key=lambda item: item[1][4], reverse = True)}
    for z in comments_sorted_dict:
        print("Rank:", comments_sorted_dict[z][0])
        print("Title:", comments_sorted_dict[z][1])
        print("Points:", comments_sorted_dict[z][2])
        print("Time:", comments_sorted_dict[z][3])
        print("Comment #:", comments_sorted_dict[z][4])
        print("=" * 80)
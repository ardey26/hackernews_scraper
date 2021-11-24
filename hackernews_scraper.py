from bs4 import BeautifulSoup
import requests


sort_by_points = False
sort_by_comment = False
sort_by_default = False

news_dict = {}
results = int(input("How many results do you want: "))
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

choice = int(input("[1] - SORT BY POINTS | [2] - SORT BY COMMENT | [3] - DEFAULT: "))
if choice == 1:
    sort_by_points = True

elif choice == 2:
    sort_by_comment = True

elif choice == 3:
    sort_by_default = True

if(sort_by_points):
    points_sorted_dict = {k: v for k, v in sorted(news_dict.items(), key=lambda item: item[1][2], reverse = True)}
    j = 1
    for i in points_sorted_dict:
        print("Rank:", j)
        print("Title:", points_sorted_dict[i][1])
        print("Points:", points_sorted_dict[i][2])
        print("Time:", points_sorted_dict[i][3], "hours ago")
        print("Comments:", points_sorted_dict[i][4])
        print("=" * 80)
        j += 1

if(sort_by_comment):
    comments_sorted_dict = {k: v for k, v in sorted(news_dict.items(), key=lambda item: item[1][4], reverse = True)}
    j = 1
    for z in comments_sorted_dict:
        print("Rank:", j)
        print("Title:", comments_sorted_dict[z][1])
        print("Points:", comments_sorted_dict[z][2])
        print("Time:", comments_sorted_dict[z][3],"hours ago")
        print("Comments:", comments_sorted_dict[z][4])
        print("=" * 80)
        j += 1

if(sort_by_default):
    j = 1
    for z in news_dict:
        print("Rank:", news_dict[z][0])
        print("Title:", news_dict[z][1])
        print("Points:", news_dict[z][2])
        print("Time:", news_dict[z][3],"hours ago")
        print("Comments:", news_dict[z][4])
        print("=" * 80)
        j += 1

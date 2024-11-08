from bs4 import BeautifulSoup
import requests
from datetime import datetime

def start(results):
    news_dict = {}
    result_per_page = []
    while results > 30:
        result_per_page.append(30)
        results -= 30
    result_per_page.append(results)
    
    page = 1
    while(page != len(result_per_page) + 1):
        url = f"https://news.ycombinator.com/news?p={page}"
        r = requests.get(url)
        html = r.content
        soup = BeautifulSoup(html, 'lxml')
        news_score = soup.find_all("tr", class_ = "athing")
        news_subtext = soup.find_all("td", class_ = "subtext")

        for i in range(result_per_page[page - 1]):
            j = news_score[i]['id'] # id value
            score = f"score_{j}"
            comments = f"item?id={j}"
            k1 = news_score[i].find("span", class_ = "rank").text[:-1] # news rank
            k2 = news_score[i].find("a", class_ = "titlelink").text # news title
            k41 = soup.find_all(href = comments) 
            try:
                k3 = soup.find(id = score).text # Score by id
                k3 = int(k3.split(" ")[0])
            except AttributeError:
                k3 = 0
            try:
                k4 = news_subtext[i].find("span", class_ = "age")["title"][11:] # Time Posted
            except ValueError:
                k4 = 0

            try:
                k5 = int(k41[-1].text[:-9]) # Comment number
            except ValueError:
                k5 = 0
            k6 = news_subtext[i].find("span", class_ = "age")["title"][:-9]
            news_dict[j] = [k1, k2, k3, k4, k5, k6]
        page += 1
    return news_dict

def sort_by_points(dict_param):
    points_sorted_dict = {k: v for k, v in sorted(dict_param.items(), key=lambda item: item[1][2], reverse = True)}
    rank = 1
    for i in points_sorted_dict:
        print("Rank:", rank)
        print("Title:", points_sorted_dict[i][1])
        print("Points:", points_sorted_dict[i][2])
        print("Comments:", points_sorted_dict[i][4])
        print("Time: ", points_sorted_dict[i][3])
        print("Date:", points_sorted_dict[i][5])
        print("=" * 80)
        rank += 1

def sort_by_comment(dict_param):
    comments_sorted_dict = {k: v for k, v in sorted(dict_param.items(), key=lambda item: item[1][4], reverse = True)}
    rank = 1
    for item in comments_sorted_dict:
        print("Rank:", rank)
        print("Title:", comments_sorted_dict[item][1])
        print("Points:", comments_sorted_dict[item][2])
        print("Comments:", comments_sorted_dict[item][4])
        print("Time: ", comments_sorted_dict[item][3])
        print("Date:", comments_sorted_dict[item][5])
        print("=" * 80)
        rank += 1

def sort_by_default(dict_param):
    for item in dict_param:
        print("Rank:", dict_param[item][0])
        print("Title:", dict_param[item][1])
        print("Points:", dict_param[item][2])
        print("Comments:", dict_param[item][4])
        print("Time: ", dict_param[item][3])
        print("Date:", dict_param[item][5])
        print("=" * 80)

def sort_by_newest(dict_param):
    newest_sorted_dict = {k: v for k, v in sorted(dict_param.items(), key=lambda item: datetime.strptime(item[1][5], "%Y-%m-%d"), reverse = True)}
    rank = 1
    for item in newest_sorted_dict:
        print("Rank:", newest_sorted_dict[item][0])
        print("Title:", newest_sorted_dict[item][1])
        print("Points:", newest_sorted_dict[item][2])
        print("Comments:", newest_sorted_dict[item][4])
        print("Time: ", newest_sorted_dict[item][3])
        print("Date:", newest_sorted_dict[item][5])
        print("=" * 80)
        rank += 1

def sort_by_oldest(dict_param):
    oldest_sorted_dict = {k: v for k, v in sorted(dict_param.items(), key=lambda item: datetime.strptime(item[1][5], "%Y-%m-%d"))}
    rank = 1
    for item in oldest_sorted_dict:
        print("Rank:", oldest_sorted_dict[item][0])
        print("Title:", oldest_sorted_dict[item][1])
        print("Points:", oldest_sorted_dict[item][2])
        print("Comments:", oldest_sorted_dict[item][4])
        print("Time: ", oldest_sorted_dict[item][3])
        print("Date:", oldest_sorted_dict[item][5])
        print("=" * 80)
        rank += 1

if __name__ == "__main__":
    amount = int(input("RESULT AMOUNT: "))
    results_dict = start(amount)

    choice = int(input("[1] - SORT BY POINTS | [2] - SORT BY COMMENT | [3] - DEFAULT | [4] - NEWEST | [5] - OLDEST: "))

    choice -= 1
    choice_handlers = [sort_by_points, sort_by_comment, sort_by_default, sort_by_newest, sort_by_oldest]

    chosen_choice_handler = choice_handlers[choice]

    return chosen_choice_handler(results_dict)    

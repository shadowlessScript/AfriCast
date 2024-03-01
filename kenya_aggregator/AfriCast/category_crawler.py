import requests
from bs4 import BeautifulSoup
from .news_crawler import url_list


cat_article_list = []


def category_crawler(url, category):
    if category == "business":
        if url == "https://www.tuko.co.ke":
            url += f"/{category}-economy"
        elif url == "https://nairobiwire.com":
            url += "/category/business"
        elif url == "https://www.businessdailyafrica.com":
            url += "/bd/markets"
        else:
            url += f"/{category}"
    elif category == 'politics':
        if url =="https://www.the-star.co.ke":
            url += "/siasa"
        elif url == "https://nairobiwire.com" or url == "https://newstrends.co.ke":
            url += "/category/politics"
        else:
            url += f"/{category}"
    elif category == "sports":
        if url == "https://nairobiwire.com" or url == "https://newstrends.co.ke":
            url += "/category/sports"
        elif url == "https://www.theeastafrican.co.ke":
            url += f'/tea/{category}'
        else:
            url += f"/{category}"
    else:
        if url == "https://nairobiwire.com":
            url += f"/category/{category}"
        elif url == "https://www.the-star.co.ke":
            url += "/sasa/entertainment/"
        elif url == "https://nation.africa/kenya":
            url += "/life-and-style/culture"
        else:
            url += f"/{category}"

    from collections import OrderedDict

    request = requests.get(url)

    if request.status_code == 200:
        scraper = BeautifulSoup(request.content, "html.parser")

        temp_articles = scraper.find_all("article") or scraper.find_all("h3")  # a list of all the article/h3 tags

        if len(temp_articles) == 1:
            if url == "https://www.theeastafrican.co.ke/tea/sports":
                temp_articles = scraper.find_all("section", "main-home-content", recursive=True)
                for t in temp_articles:
                    temp_articles = t.find_all("h3")
            else:
                temp_articles = scraper.find_all("h3")

        repo = {"source": url, "news": [], "links": [], "images": []}
        if len(temp_articles) > 20 and url != "https://www.theeastafrican.co.ke/tea/sports":
            a = round(len(temp_articles)/3)
            articles = temp_articles[a:]
        else:
            articles = temp_articles[:]
        if articles:
            counter = 0

            for article in articles:
                repo["news"] = list(OrderedDict.fromkeys(repo["news"])) # removing duplicates, without changing the
                # values index
                repo["links"] = list(OrderedDict.fromkeys(repo["links"]))
                if counter < 10:  # limiting the news headlines to only 10 per website.

                    news_links = article.find("a")
                    images = article.find("img")
                    if not news_links:  # if no link is found in the <article> tag
                        if article.parent.name == "a":
                            # checks if the parent name for the article tag is an 'a' tag i.e
                            # <a href='...'><article></article></a>
                            news_links = article.parent
                        else:
                            # check the parent element for an "a" tag
                            news_links = article.parent.find("a")
                            if not news_links:
                                news_links = article.parent.parent.find("a")
                                # repo["links"].append(news_links["href"])
                            # repo["news"].append(news_links.text)

                    if news_links["href"].startswith("https:"):
                        # checks if the href is an url or a path i.e <a href="www.websit.co.ke/tech/new-tech"></a> or <a
                        # href="/tech/new-tech></a>"
                        repo["links"].append(news_links["href"])
                    else:
                        if (url == "https://nation.africa/kenya/sports"
                                or url == "https://nation.africa/kenya/life-and-style/culture"):
                            url = "https://nation.africa"
                        url_temp = url.split("/")  # ["https:","","domain-name"] -> https://domain-name
                        news_links_temp = news_links["href"].split(
                            "/")  # ["","subdirectory","some-headline"] -> /subdirectory/some-headline

                        # Check if the last element of 'url_temp' matches the second element of 'news_links_temp'

                        if (url_temp[len(url_temp) - 1] == news_links_temp[1]
                                or url_temp[len(url_temp) - 2:] == news_links_temp[1:3]):
                            # The website 'www.nation.africa/kenya' starts its paths with '/kenya/some-story'. If these
                            # paths are combined, it results in 'www.nation.africa/kenya/kenya/some-story' which gives a
                            # 404 response. To avoid this, the last element from 'url_temp', which is "kenya", is removed.
                            if url_temp[len(url_temp) - 2:] == news_links_temp[1:3]:
                                url_temp.remove(url_temp[len(url_temp) - 1])
                                url_temp.remove(url_temp[len(url_temp) - 1])
                            else:
                                url_temp.remove(url_temp[len(url_temp) - 1])

                            # The elements of 'url_temp' are then joined into a string separated by '/'.
                            url_temp = "/".join(url_temp)

                            # The combined URL and the 'href' attribute from 'news_links' are appended to the 'links'
                            # list in 'repo'.
                            repo["links"].append(f'{url_temp}{news_links["href"]}')
                        else:
                            repo["links"].append(f'{url}{news_links["href"]}')

                    if images:
                        if images.has_attr("src"):
                            repo["images"].append(images["src"])
                        else:
                            repo["images"].append(images["data-src"])
                    else:
                        repo["images"].append("image not found")
                    repo["news"].append(article.get_text())
                else:
                    break
                counter += 1

            cat_article_list.append(repo)


def start_category_crawler(category):
    for url in url_list:
        category_crawler(url, category)
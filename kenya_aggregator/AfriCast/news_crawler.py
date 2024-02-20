import requests
from bs4 import BeautifulSoup
# from newspaper import Article

url_list = [
    "https://www.tuko.co.ke",
    "https://nation.africa/kenya",
    "https://www.the-star.co.ke",
    "https://mpasho.co.ke",
    "https://www.businessdailyafrica.com",
    "https://nairobiwire.com",
    "https://newstrends.co.ke",
    "https://www.theeastafrican.co.ke",
]

article_list = []


def scrape_website(url):
    """
    extracts all the <article>/<h3> tags in the given url,
    in each tag the news link and story headline are extracted.

    :param url: website url
    :type url: str
    """

    try:
        request = requests.get(url)

        if request.status_code == 200:
            scraper = BeautifulSoup(request.content, "html.parser")

            articles = scraper.find_all("article") or scraper.find_all("h3")  # a list of all the article/h3 tags

            if len(articles) == 1:
                articles = scraper.find_all("h3")

            repo = {"source": url, "news": [], "links": [], "images": []}

            counter = 0
            if articles:
                for article in articles:
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
                            url_temp = url.split("/")  # ["https:","","domain-name"] -> https://domain-name
                            news_links_temp = news_links["href"].split(
                                "/")  # ["","subdirectory","some-headline"] -> /subdirectory/some-headline

                            # Check if the last element of 'url_temp' matches the second element of 'news_links_temp'

                            if url_temp[len(url_temp) - 1] == news_links_temp[1]:
                                # The website 'www.nation.africa/kenya' starts its paths with '/kenya/some-story'. If these
                                # paths are combined, it results in 'www.nation.africa/kenya/kenya/some-story' which gives a
                                # 404 response. To avoid this, the last element from 'url_temp', which is "kenya", is removed.
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
                article_list.append(repo)
    except Exception:
        pass

def start_crawler():
    for url in url_list:
        scrape_website(url)

    # trending()

def trending():
    if article_list:

        # make an algorithm that, finds similarities scores in the news titles.

        # import required libraries
        import pandas as pd
        import numpy
        from sklearn.feature_extraction.text import TfidfVectorizer as Tfidf
        from sklearn.metrics.pairwise import linear_kernel
        from collections import Counter

        # make a dataframe for the article_list var
        articles_df = pd.DataFrame(article_list)

        # initialise the text feature extractor model
        tfidf = Tfidf(stop_words="english")

        the_tea = []  # stores the unpacked news list of each source

        for news_lst in articles_df["news"]:
            # articles_df['news'] -> [ [some headlines...], [some other headlines...],.....[] ]
            for news in news_lst:
                # news_list -> [some headlines]
                the_tea.append(news)  # news -> "a headline"

        tfidf_matrix = tfidf.fit_transform(the_tea)
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        indices = pd.Series(the_tea)

        # Count occurrences of each headline
        headline_counts = Counter(the_tea)

        # Sort headlines by frequency (most common to least common)
        trending_headlines = headline_counts.most_common()

        def get_trending(i):
            # ind = indices.
            trending_lst = []
            sim_score = enumerate(cosine_sim[i])
            sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)
            sim_score = sim_score[1:]
            cleaned_sim_score = [x for x in sim_score if x[1] >= 0.9]
            sim_index = [x[0] for x in cleaned_sim_score]

            trending_lst.append(sim_index)

            return trending_lst
        # for i in range(len(the_tea)):
        #     get_trending(i)
        # sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)

    else:
        start_crawler()
        trending()



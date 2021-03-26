import requests
from bs4 import BeautifulSoup

NEWS_RESOURCE = 'news'
LINK_NEWS_CLASS = 'nw-o-link-split__anchor'


def bbc_parse(url):
    cats = get_categories_urn(get_html(url + '/' + NEWS_RESOURCE))
    links = get_all_articles_links(cats, url, LINK_NEWS_CLASS)
    articles_text = get_articles(links)
    return articles_text


def get_html(url):
    response = requests.get(url)
    return response.text


def get_categories_urn(html_code):
    soup = BeautifulSoup(html_code, 'html.parser')
    categories_urn = []
    for category in soup.find_all('a', class_='nw-o-link'):
        categories_urn.append(category['href'])
    return categories_urn


def get_all_articles_links(categories_urn, url, link_news_class):
    cat_links = []
    for cat in categories_urn:
        cat_links.append(url + cat)
    all_links = []
    link_count = 0
    for cat_link in cat_links:
        html_code_cat = get_html(cat_link)
        soup = BeautifulSoup(html_code_cat, 'html.parser')
        link_count += 1
        for news_link in soup.find_all('a', class_=link_news_class):
            all_links.append(news_link['href'])
        if link_count >= 10:
            return set(prepare_links(all_links, url))
    return set(prepare_links(all_links, url))


def prepare_links(links, url):
    for i, article_link in enumerate(links):
        if article_link.startswith('//'):
            article_link = article_link[2:]

        if article_link.startswith('/'):
            article_link = article_link[1:]

        if not article_link.startswith(url):
            article_link = url + article_link

        links[i] = article_link
    return links


def get_articles(all_links):
    articles = []
    for i, link in enumerate(all_links):
        if requests.get(link).status_code == 200:
            html = get_html(link)
            soup = BeautifulSoup(html, 'html.parser')
            h1 = soup.h1
            if h1 is None:
                h1 = ''
            else:
                h1 = h1.get_text()
            article = soup.article
            if article is not None:
                articles.append({
                    'title': h1,
                    'link': link,
                    'content': article.get_text()
                })
    return articles

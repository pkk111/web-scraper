import string

import requests
from bs4 import BeautifulSoup
import os


def get_response(url):
    r = requests.get(url)
    response = r.json()
    if r.status_code == 200 and 'content' in response.keys():
        print(response['content'])
    else:
        print("Invalid quote resource!")


def get_movies(url):
    if url == 'https://www.imdb.com/title/tt0068646/':
        url = 'https://web.archive.org/web/20211101044320/https://www.imdb.com/title/tt0068646/'
    r = requests.get(url,  headers={'Accept-Language': 'en-US,en;q=0.5'})
    if 'title' not in url or r.status_code != 200:
        print('Invalid movie page!')
        return
    soup = BeautifulSoup(r.content, 'html.parser')
    movie = {"title": soup.find('title').text, "description": soup.find('meta', {'name': 'description'})['content']}
    print(movie)


def save_page(url):
    r = requests.get(url)
    if r.status_code == 200:
        page_content = r.content
        with open('source.html', 'wb') as file:
            file.write(page_content)
            print("Content saved.")
    else:
        print(f"The URL returned {r.status_code}")


def save_files(url):
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        articles = soup.find_all('article')
        tag_to_search = "News"
        for article in articles:
            if article.find('span', "c-meta__type").text == tag_to_search:
                dis = article.find('div', {'itemprop': "description"}).text.strip()
                article_link = "https://www.nature.com" + article.find('a', {'data-track-action': "view article"})['href']
                article_soup = BeautifulSoup(requests.get(article_link).content, 'html.parser')
                body = article_soup.find('div', {'class': "c-article-body u-clearfix"})
                title = article.find('h3', {'itemprop': "name headline"}).text.strip()
                title = "".join([word for word in title if word not in string.punctuation]).replace(" ", "_")
                with open(title + ".txt", 'wb') as file:
                    file.write(body.text.strip().encode('UTF-8'))
    else:
        print(f"The URL returned {r.status_code}")


def save_pages(art_type, pages):
    for n in range(pages):
        url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&Page={}".format(n+1)
        r = requests.get(url)
        folder = f"Page_{n+1}"
        os.mkdir(folder)
        os.chdir(folder)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            articles = soup.find_all('article')
            for article in articles:
                if article.find('span', "c-meta__type").text == art_type:
                    article_link = "https://www.nature.com" + article.find('a', {'data-track-action': "view article"})['href']
                    article_soup = BeautifulSoup(requests.get(article_link).content, 'html.parser')
                    body = article_soup.find('div', {'class': "c-article-body u-clearfix"})
                    title = article.find('h3', {'itemprop': "name headline"}).text.strip()
                    title = "".join([word for word in title if word not in string.punctuation]).replace(" ", "_")
                    with open(title + ".txt", 'wb') as file:
                        file.write(body.text.strip().encode('UTF-8'))
        else:
            print(f"The URL returned {r.status_code}")
        os.chdir('..')


if __name__ == '__main__':
    pages = int(input())
    art_type = input()
    save_pages(art_type, pages)

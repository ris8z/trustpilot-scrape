import requests 
from bs4 import BeautifulSoup
import time


def scrape(url):
    response = requests.get(url)
    if response.status_code == 404:
        raise Exception("so finite le pagine")
    return response.text

def get_author(r):
    author_span = r.find('span', attrs={'data-consumer-name-typography':True})
    if not author_span:
        return None
    author_value = author_span.get_text(strip=True)
    return author_value

def get_rating(r):
    rating_div = r.find('div', attrs={'data-service-review-rating':True})
    if not rating_div:
        return None
    rating_value = rating_div['data-service-review-rating']
    return rating_value

def get_title(r):
    title_h2 = r.find('h2', attrs={'data-service-review-title-typography':True})
    if not title_h2:
        return None
    title_value = title_h2.get_text(strip=True)
    return title_value

def get_content(r):
    content_p = r.find('p', attrs={'data-service-review-text-typography': True})
    if not content_p:
        return None
    content_value = content_p.get_text(strip=True)
    return content_value

def get_date(r):
    date_p = r.find('p', attrs={'data-service-review-date-of-experience-typography':True})
    if not date_p:
        return None
    date_value = date_p.get_text(strip=True)
    return date_value.split(":")[-1]


def parse(html_page):
    bsMagic = BeautifulSoup(html_page, 'html.parser')
    reviews = bsMagic.find_all('article')

    lst = []
    for r in reviews:
        d = {
            'author': get_author(r),
            'rating' : get_rating(r),
            'title' : get_title(r),
            'content' : get_content(r),
            'date' : get_date(r)
        }
        lst.append(d)
    return lst

def output(results):
    for r in results:
        print(r,",")

def main():
    n = 0
    page = 1
    try:
        while True:
            url = f"https://www.trustpilot.com/review/hostingpower.ie?page={page}"
            html = scrape(url)
            res = parse(html)
            output(res)
            n += len(res)
            page += 1
            time.sleep(5)
    except Exception as e:
        print(e)
    finally:
        print(f"got {n} reviews")

if __name__ == "__main__":
    main()

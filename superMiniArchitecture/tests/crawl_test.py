import requests
from bs4 import BeautifulSoup
import pandas as pd


base_url="https://vnexpress.net/thoi-su"
headers={
    'User-Agent': "Mozilla/5.0 (Linux; Android 16; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.12.45 Mobile Safari/537.36"

}

# tao list rong de luu data

data_crawled = []
response = requests.get(base_url, headers=headers, timeout=10)
response.raise_for_status() # tu dong bao loi neu khong vao duoc web

# boc tach
soup = BeautifulSoup(response.text, 'html.parser')
articles=soup.find_all('article',class_='item-news')

for article in articles:

    title_tag = article.find('h3',class_='title-news').find('a')
    if title_tag:
        title = title_tag.get('title')
        link=title_tag.get('href')
        if title and link:

            if not link.startswith('http'):
                link=base_url + link

            data_crawled.append({
                'TieuDe':title.strip(),
                'DuongDan':link
            
            })

    df = pd.DataFrame(data_crawled)

    df.to_csv('vnexpress_new.csv', index=False, encoding='utf-8-sig')
    print(f'Da hoan thanh! da luu {len(data_crawled)} tin vao "vnexpress_new.csv')


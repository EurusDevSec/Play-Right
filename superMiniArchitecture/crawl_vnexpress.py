import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def main():
    url = "https://vnexpress.net"


    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"Dang gui request den {url}")

    try:

        reponse = requests.get(url, headers=headers, timeout=10)
        reponse.raise_for_status()
        print("REquest thanh cong! Dang boc tach html...")
        
        # buoc 3 boc tach (parse)
        articles = BeautifulSoup.find_all('article', class_='item-news')
        data_crawled = []


        for article in articles:
            title_element = article.find('h3', class_ = "title-news")
            link_element = article.find('a')


            if title_element and link_element:
                title = title_element.text.strip()
                link=link_element('href')

                if title and link:
                    data_crawled.append({
                        'TieuDe':title,
                        'DuongDan': link
                    })

        if not data_crawled:
            print("Lỗi: Không tìm thấy bài viết nào. Cần kiểm tra lại 'selector' (class_)")
            return
        print(f"Da crawl thanh cong { len(data_crawled)} bai viet")


        #buoc 4 luu data
        df = pd.DataFrame(data_crawled)
        df.to_csv('vnexpress_data.csv', index=False, encoding='utf-8-sig')
        print("Da xong ! du lieu duoc luu vao file 'vnexpress_data.csv")


    except requests.exceptions.HTTPError as errh:
        print(f"loi http: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"loi ket noi: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Lỗi Timeout: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Lỗi Request: {err}")
    except Exception as e:
        print(f"Một lỗi không xác định đã xảy ra: {e}")

if __name__ == "__main__":
    main()
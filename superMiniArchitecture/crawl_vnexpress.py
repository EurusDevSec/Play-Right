import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def main():
   #dinh nghia muc tieu can crawl
    base_url = "https://vnexpress.net"
    
   
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"Đang gửi request đến {base_url}...")
    
    try:
        # buoc 2: gui request
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status() # Báo lỗi nếu request thất bại

        print("Request thành công! Đang bóc tách HTML...")

        # BƯỚC 3: BÓC TÁCH 
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # **Đây là selector chính**: Tìm tất cả các thẻ <article> có class 'item-news'
        articles = soup.find_all('article', class_='item-news')
        
        data_crawled = []

        print(f"Tìm thấy {len(articles)} bài viết. Đang bóc tách...")

        for article in articles:
            # Tìm thẻ <h3> có class 'title-news' bên trong mỗi bài viết
            title_element = article.find('h3', class_='title-news')
            
            if title_element:
                # Tìm thẻ <a> bên trong thẻ <h3> đó
                link_element = title_element.find('a')
                
                if link_element:
                    # Lấy tiêu đề từ thuộc tính 'title' của thẻ <a>
                    title = link_element.get('title')
                    # Lấy link từ thuộc tính 'href' của thẻ <a>
                    link = link_element.get('href')

                    # Đảm bảo có cả hai
                    if title and link:
                        
                        # **Best Practice**: Xử lý link tương đối
                        if not link.startswith('http'):
                            link = base_url + link
                            
                        data_crawled.append({
                            'TieuDe': title.strip(),
                            'DuongDan': link
                        })

        if not data_crawled:
            print("Lỗi: Không tìm thấy bài viết nào. Selector có thể đã thay đổi.")
            return

        print(f"Đã crawl thành công {len(data_crawled)} bài viết.")

        # BƯỚC 4: LƯU TRỮ (LOAD)
        df = pd.DataFrame(data_crawled)
        
        # 'utf-8-sig' để Excel đọc file tiếng Việt không bị lỗi font
        df.to_csv('vnexpress_data.csv', index=False, encoding='utf-8-sig')
        
        print("---")
        print("✅ ĐÃ HOÀN THÀNH! Dữ liệu đã được lưu vào file 'vnexpress_data.csv'")
        print("---")

    except requests.exceptions.HTTPError as errh:
        print(f"Lỗi HTTP: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Lỗi Kết nối: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Lỗi Timeout: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Lỗi Request: {err}")
    except Exception as e:
        print(f"Một lỗi không xác định đã xảy ra: {e}")

if __name__ == "__main__":
    main()
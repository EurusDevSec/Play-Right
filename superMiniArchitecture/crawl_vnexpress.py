import requests
from bs4 import BeautifulSoup
import pandas as pd
def main():
   #dinh nghia muc tieu can crawl
    base_url = "https://vnexpress.net"
    
    # du dung target url voi cac link tuy chon 
    target_url = "https://vnexpress.net/thoi-su"
    # su dung user-agent gia lap trinh duyet de tranh bi server chan bot 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    LIMIT = 40
    print(f"Đang gửi request đến {base_url}...")
    

    # buoc 2: gui request
    response = requests.get(target_url, headers=headers, timeout=10)
    response.raise_for_status() #bao bat ky loi nao xay ra nhu 404, 503, bad request tranh crash

    print("Request thành công! Đang bóc tách HTML...")

    # buoc3: boc tach
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = soup.find_all('article', class_='item-news')
    print(articles)
    data_crawled = []
    
    # in ra so luong bai viet co LIMIT lam gioi han
    print(f"Tìm thấy {len(articles)} bài viết. Đang bóc tách {LIMIT} bai viet...")
    # duyet qua tung article trong danh sach articles lay duoc 
    for article in articles:
        # kiem tra gioi han neu vuot qua limit thi break
        if len(data_crawled) >= LIMIT:
            print(f"Da dat gioi han {LIMIT} BAI VIET. Dung crawl")
            break
        # su dung phuong thuc find tim the h3 dua tren class title-news
        title_element = article.find('h3', class_='title-news')
        
        image_element = article.find('img')
        if title_element:
           
            link_element = title_element.find('a')
            
            if link_element:
              
                title = link_element.get('title')
             
                link = link_element.get('href')

              
                if title and link:
                    if not link.startswith('http'):
                        link = base_url + link
                        
                    image_url =image_element.get('src') if image_element else ""
                    data_crawled.append({
                        'TieuDe': title.strip(),
                        'DuongDan': link,
                        'HinhAnh': image_url
                    })

    if not data_crawled:
        print("Lỗi: Không tìm thấy bài viết nào. Selector có thể đã thay đổi.")
        return

    print(f"Đã crawl thành công {len(data_crawled)} bài viết.")

    # luu
    df = pd.DataFrame(data_crawled)
    
    # 'utf-8-sig' để Excel đọc file tiếng Việt không bị lỗi font
    df.to_csv('vnexpress_data.csv', index=False, encoding='utf-8-sig')
    print(f"✅ ĐÃ HOÀN THÀNH! {len(data_crawled)} Dữ liệu đã được lưu vào file 'vnexpress_data.csv'")
  



if __name__ == "__main__":
    main()
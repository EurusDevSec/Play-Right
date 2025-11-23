import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
def main():
   #dinh nghia muc tieu can crawl
    base_url = "https://vnexpress.net"
    
    # du dung target url voi cac link tuy chon 
    target_url = [
        "https://vnexpress.net/phap-luat",
        "https://vnexpress.net/giai-tri",
        "https://vnexpress.net/suc-khoe"
    ]
    # su dung user-agent gia lap trinh duyet de tranh bi server chan bot 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    LIMIT = 20
    data_crawled = []
    print(f"Đang gửi request đến {base_url}...")
    for url in target_url:
        print(f"---Dang xu ly chuyen muc: {url}")
        try:
            

            # buoc 2: gui request
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status() #bao bat ky loi nao xay ra nhu 404, 503, bad request tranh crash

            print("Request thành công! Đang bóc tách HTML...")

            # buoc3: boc tach
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = soup.find_all('article', class_='item-news')
            print(articles)
            count=0
            
            # in ra so luong bai viet co LIMIT lam gioi han
            print(f"Tìm thấy {len(articles)} bài viết. Đang bóc tách {LIMIT} bai viet...")
            # duyet qua tung article trong danh sach articles lay duoc 
            for article in articles:
                # kiem tra gioi han neu vuot qua limit thi break
                if count >= LIMIT:
                    print(f"Da dat gioi han {LIMIT} BAI VIET. Dung crawl")
                    break
                # su dung phuong thuc find tim the h3 dua tren class title-news
                title_element = article.find('h3', class_='title-news')
                # tim the img de lay anh
                image_element = article.find('img')

                
                # Lay Mo ta ngan (Sapo)
                sapo_tag = article.find('p', class_='description')
                sapo = sapo_tag.find('a').get_text(strip=True) if sapo_tag and sapo_tag.find('a') else ""
                
                # Lay Thoi gian
                time_tag = article.find('span', class_='time-ago')
                publish_time = time_tag.get_text(strip=True) if time_tag else "Mới cập nhật"

                # Phan loai
                category = url.split('/')[-1].replace('-', ' ').title()
                # --------------------

                if title_element:
                
                    link_element = title_element.find('a')
                    
                    if link_element:
                    
                        title = link_element.get('title')
                    
                        link = link_element.get('href')

                    
                        if title and link:
                            if not link.startswith('http'):
                                link = base_url + link
                                
                            
                            # VnExpress hay dùng data-src cho lazy load
                            image_url = image_element.get('data-src') if image_element and image_element.get('data-src') else (image_element.get('src') if image_element else "")

                            data_crawled.append({
                                'ChuyenMuc': category,
                                'TieuDe': title.strip(),
                                'MoTa': sapo,
                                'ThoiGian': publish_time,
                                'DuongDan': link,
                                'HinhAnh': image_url
                            })
                            count += 1
            # neu khong co bai nao thi in loi va return 
            if count == 0:
                print("Lỗi: Không tìm thấy bài viết nào trong mục này.")
        except Exception as e:
            print(f"😣 Loi khi crawl {url}: {e}")
    print(f"Đã crawl thành công {len(data_crawled)} bài viết.")


    # luu
    df = pd.DataFrame(data_crawled)
    
    # 'utf-8-sig' để Excel đọc file tiếng Việt không bị lỗi font
    df.to_csv('vnexpress_advanced.csv', index=False, encoding='utf-8-sig')
    print(f"✅ ĐÃ HOÀN THÀNH! {len(data_crawled)} Dữ liệu đã được lưu vào file 'vnexpress_advanced.csv'")
  



if __name__ == "__main__":
    main()
BÁO CÁO ĐỀ TÀI CRAWLING DATA

Dự án: Xây dựng Pipeline Thu thập và Trực quan hóa Tin tức

Môn học: Thực hành [Tên môn học của bạn]
Đề tài: [QT1] Trình bày nhóm (Crawling data)
Ngày: 15/11/2025

1. Giới thiệu

Thu thập dữ liệu web (web crawling) là một kỹ năng nền tảng trong lĩnh vực khoa học dữ liệu và kỹ thuật phần mềm. Đây là bước đầu tiên để trích xuất thông tin thô từ vô số các trang web, biến chúng thành dữ liệu có cấu trúc để phục vụ cho việc phân tích, lưu trữ hoặc xây dựng ứng dụng.

Với yêu cầu của đề tài [QT1], nhóm đã quyết định thực hiện một pipeline thu thập dữ liệu hoàn chỉnh. Thay vì chỉ dừng lại ở việc lấy dữ liệu thô, nhóm đã mở rộng mục tiêu:

Crawl (Thu thập): Lấy dữ liệu tin tức (Tiêu đề, Đường link, Hình ảnh) từ một trang báo uy tín (VnExpress).

Save (Lưu trữ): Lưu trữ dữ liệu đã được làm sạch vào một file có cấu trúc (.csv).

2. Phương pháp và Công cụ sử dụng

Để đảm bảo dự án được hoàn thành đúng thời hạn và có sản phẩm chạy được 100%, nhóm đã áp dụng phương pháp "Bắt đầu đơn giản" (Start Simple) hay "Sản phẩm Khả thi Tối thiểu" (MVP). Nhóm tập trung vào các trang web tĩnh và sử dụng một bộ công cụ (tech stack) linh hoạt, hiệu quả, hoàn toàn bằng Python.

Các công cụ chính được sử dụng:

Ngôn ngữ: Python 3.

Quản lý môi trường: uv (thay cho pip/venv) để cài đặt thư viện nhanh chóng.

Gửi yêu cầu HTTP: Thư viện requests để tải nội dung HTML của trang web.

Bóc tách HTML (Parsing): Thư viện BeautifulSoup4 để lọc và tìm kiếm các thẻ HTML cần thiết.

Xử lý và Lưu trữ Dữ liệu: Thư viện pandas để tổ chức dữ liệu vào DataFrame và xuất ra file CSV.

3. Kiến trúc và Thực thi

Quy trình của nhóm: Script Thu thập (Backend)

3.1. Script Thu thập (crawl_vnexpress.py)

Đây là file chịu trách nhiệm lấy dữ liệu.

Xác định Mục tiêu: Nhóm chọn https://vnexpress.net/thoi-su làm URL mục tiêu. bất kì url nào sau vnexpress.net cũng được định nghĩa để xử lý các đường link tương đối.

Giả lập Trình duyệt: Một headers (User-Agent) được khai báo để giả lập là một trình duyệt Chrome, tránh bị website từ chối truy cập.

Gửi Request: Dùng requests.get() để tải toàn bộ HTML. Lệnh response.raise_for_status() được dùng như một "chốt an toàn" (best practice) để tự động báo lỗi nếu website trả về 4xx hoặc 5xx.

Bóc tách Dữ liệu:

Nhóm đã phân tích cấu trúc DOM (HTML) của VnExpress và phát hiện ra rằng mọi tin tức đều được bọc trong thẻ <article class='item-news'>.

Chúng ta dùng soup.find*all('article', class*='item-news') để lấy ra một danh sách (list) tất cả các khối tin.

Lọc và Làm sạch:

Nhóm duyệt qua từng khối article trong danh sách.

Để chống lỗi (crash) khi gặp quảng cáo (không có tiêu đề), nhóm áp dụng 2 lớp kiểm tra if title_element: và if link_element: (lập trình phòng thủ).

Tiêu đề: Lấy từ thuộc tính title của thẻ <a>.

Đường link: Lấy từ thuộc tính href của thẻ <a>. Code cũng tự động kiểm tra link.startswith('http') để nối base_url vào nếu link bị thiếu.

Hình ảnh: Lấy từ thuộc tính src của thẻ <img> đầu tiên.

Lưu trữ: Dữ liệu sạch (Tiêu đề, Đường link, Hình ảnh) được append vào một list, sau đó dùng pandas.DataFrame() để tạo bảng và lưu ra file vnexpress_with_images.csv với encoding='utf-8-sig' để đảm bảo tiếng Việt hiển thị chính xác trên Excel.

5. Hạn chế và Hướng phát triển

Giải pháp hiện tại (requests + BeautifulSoup) rất hiệu quả cho các trang web tĩnh (static HTML) nhưng là không đủ cho các bài toán phức tạp trong thực tế.

Hạn chế:

Trang web động (Dynamic): Script sẽ thất bại hoàn toàn với các trang web như TopCV, ITviec, hoặc Facebook, nơi mà dữ liệu được tải bằng JavaScript (JS) sau khi trang đã hiển thị.

Lưu trữ: File CSV không có khả năng mở rộng. Nếu crawl 1 triệu bài báo, file sẽ rất lớn và truy vấn chậm.

Xử lý dữ liệu: Chúng ta mới chỉ lấy dữ liệu. Chúng ta chưa xử lý nó (ví dụ: bóc tách kỹ năng từ mô tả công việc).

Hướng phát triển (Tầm nhìn):
Nếu được phát triển thành một dự án lớn (ví dụ: Phân tích Thị trường Việc làm), nhóm đề xuất một kiến trúc E-T-L (Extract-Transform-Load) nâng cao hơn:

Extract (Thu thập): Dùng Scrapy (để crawl bất đồng bộ tốc độ cao) kết hợp với Playwright (để giả lập trình duyệt, chạy JavaScript, và vượt qua anti-bot).

Transform (Biến đổi): Dùng spaCy (thư viện NLP) để xử lý văn bản, bóc tách các kỹ năng (Python, SQL,...) từ mô tả công việc.

Load (Lưu trữ/Hiển thị): Lưu dữ liệu vào SQLite hoặc PostgreSQL (thay vì CSV) và dùng Plotly hoặc Streamlit để vẽ các biểu đồ phân tích chuyên sâu (ví dụ: Top 10 kỹ năng đang hot, Biểu đồ lương theo kinh nghiệm).

6. Kết luận

Qua đề tài [QT1], nhóm đã hoàn thành yêu cầu thu thập dữ liệu bằng cách xây dựng một pipeline đơn giản nhưng hiệu quả.

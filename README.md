Group: 16

> [!TIP]
> 1 - EurusDevSec - 2224802010279

> [!NOTE]
> 2 - Nguyen Van Linh

> [!IMPORTANT]
> 3 - Nguyen Ngoc Hoa

- Workflow - use uv (Best Practices)

### Cài đặt uv

1. **Cài đặt uv (nếu chưa có):** `pip install uv`

### Khởi tạo và quản lý dự án

3. **Khởi tạo dự án (nếu mới):** `uv init` (tạo `pyproject.toml` và cấu trúc cơ bản).
4. **Thêm dependencies:** Sử dụng `uv add` để thêm gói một cách an toàn và tự động cập nhật `pyproject.toml`:
   - `uv add pandas playwright spaCy fastapi plotly`
   - Quản lý phiên bản và dependencies tự động, tốt hơn cách cũ.

### Chạy ứng dụng

5. **Chạy ứng dụng:** `uv run python main.py`.

### Lưu ý Best Practices

- Sử dụng `pyproject.toml` cho quản lý dependencies hiện đại.
- Luôn commit `pyproject.toml` và `uv.lock` (nếu có) để đảm bảo reproducibility.
- Kiểm tra phiên bản: `uv --version`.
- Nếu cần venv riêng: `uv venv` và kích hoạt với `source .venv/bin/activate` (trên Windows: `.venv\Scripts\activate`).

This is test Background
![myBackground](assets/imgs/testGif.gif)

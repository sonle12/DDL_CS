# 🆘 HƯỚNG DẪN XỬ LÝ LỖI CHI TIẾT

> **Tất cả các lỗi thường gặp & cách khắc phục**

---

## 1️⃣ LỖI TRONG QUÁ TRÌNH CÀI ĐẶT

### ❌ `python: command not found`

**Nguyên nhân**: Python chưa được cài đặt hoặc không trong PATH

**Giải pháp**:

**Windows:**
```bash
# 1. Tải Python từ: https://www.python.org/
# 2. Cài đặt - ✅ ĐẬU "Add Python to PATH"
# 3. Khởi động lại terminal
# 4. Kiểm tra:
python --version
```

**macOS:**
```bash
# Dùng Homebrew
brew install python3

# Kiểm tra:
python3 --version
```

**Linux (Ubuntu)**:
```bash
sudo apt update
sudo apt install python3 python3-pip

python3 --version
```

---

### ❌ `pip: command not found`

**Nguyên nhân**: pip chưa được cài đặt

**Giải pháp**:

```bash
# Cài pip
python -m ensurepip --upgrade

# Hoặc
python -m pip install --upgrade pip

# Kiểm tra:
pip --version
```

---

### ❌ `Permission denied` (macOS/Linux)

**Nguyên nhân**: Không có quyền viết

**Giải pháp**:

```bash
# Tùy chọn 1: Dùng sudo (không khuyến nghị)
sudo pip install -r requirements.txt

# Tùy chọn 2: Tạo virtual environment (KHUYẾN NGHỊ)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# hoặc
venv\Scripts\activate  # Windows

# Sau đó cài package:
pip install -r requirements.txt
```

---

## 2️⃣ LỖI KHI CÀI ĐẶT THƯ VIỆN

### ❌ `ModuleNotFoundError: No module named 'openai'` (hoặc thư viện khác)

**Nguyên nhân**: Thư viện chưa được cài đặt

**Giải pháp**:

```bash
# Cài lại tất cả thư viện
pip install -r requirements.txt --upgrade

# Hoặc cài thư viện cụ thể:
pip install openai langchain chromadb sentence-transformers fastapi uvicorn

# Kiểm tra:
python -c "import openai; print(openai.__version__)"
```

---

### ❌ `ERROR: Could not find a version that satisfies the requirement`

**Nguyên nhân**: Phiên bản Python quá cũ

**Giải pháp**:

```bash
# Kiểm tra phiên bản Python
python --version

# Cần Python 3.8+
# Nếu Python < 3.8, hãy cài Python 3.9+ từ https://www.python.org/
```

---

### ❌ `SSL: CERTIFICATE_VERIFY_FAILED`

**Nguyên nhân**: Sertifikat SSL không hợp lệ (thường trên macOS)

**Giải pháp**:

```bash
# macOS: Cài sertifikat
/Applications/Python\ 3.x/Install\ Certificates.command

# Hoặc bỏ qua SSL (không an toàn):
pip install --trusted-host pypi.python.org -r requirements.txt
```

---

## 3️⃣ LỖI LIÊN QUAN OPENAI API

### ❌ `OPENAI_API_KEY not found` hoặc `invalid_api_key_error`

**Nguyên nhân**: API key chưa được thiết lập hoặc sai

**Giải pháp**:

```bash
# 1. Lấy API key từ: https://platform.openai.com/account/api-keys
# 2. Thiết lập environment variable:

# Windows PowerShell:
$env:OPENAI_API_KEY = "sk-..."

# Windows CMD:
set OPENAI_API_KEY=sk-...

# macOS/Linux:
export OPENAI_API_KEY="sk-..."

# 3. Kiểm tra:
echo $env:OPENAI_API_KEY  # Windows PowerShell
echo $OPENAI_API_KEY      # macOS/Linux

# 4. Khởi động lại terminal & server
```

**Nếu vẫn lỗi:**

Chỉnh trực tiếp trong `config.py` (không an toàn, chỉ test):
```python
OPENAI_API_KEY = "sk-your-actual-key-here"
```

---

### ❌ `RateLimitError: Rate limit exceeded`

**Nguyên nhân**: Gửi quá nhiều request (vượt quota)

**Giải pháp**:

```bash
# 1. Chờ 1-2 phút
# 2. Kiểm tra quota: https://platform.openai.com/account/billing/overview
# 3. Giảm TOP_K_DOCUMENTS trong config.py:
TOP_K_DOCUMENTS = 3  # Thay vì 5-10
# 4. Giảm LLM_MAX_TOKENS:
LLM_MAX_TOKENS = 256  # Thay vì 1024
```

---

### ❌ `Insufficient_quota` hoặc `zero balance`

**Nguyên nhân**: Hết credit hoặc không có phương thức thanh toán

**Giải pháp**:

```bash
# 1. Truy cập: https://platform.openai.com/account/billing/overview
# 2. Thêm phương thức thanh toán (Visa/Mastercard)
# 3. Thiết lập usage limit để tránh chi phí quá cao:
#    https://platform.openai.com/account/billing/limits
```

---

### ❌ `Model gpt-4 not available` hoặc `model_not_found_error`

**Nguyên nhân**: API key không có quyền dùng gpt-4

**Giải pháp**:

```python
# Trong config.py, đổi thành model sẵn có:
LLM_MODEL_NAME = "gpt-3.5-turbo"  # Hoặc gpt-4-turbo-preview
```

---

## 4️⃣ LỖI CHROMADB & DATABASE

### ❌ `chromadb.db is locked` hoặc `database is locked`

**Nguyên nhân**: Database đang được sử dụng bởi process khác

**Giải pháp**:

```bash
# 1. Dừng tất cả các server đang chạy (Ctrl+C)
# 2. Đợi 2-3 giây
# 3. Khởi động lại:
python main.py

# 2. Hoặc xóa database & tạo mới:
# - Xóa thư mục: chroma_db/
# - Khởi động lại server (sẽ tạo mới)
```

---

### ❌ `Connection refused` khi kết nối ChromaDB

**Nguyên nhân**: ChromaDB service không chạy hoặc port sai

**Giải pháp**:

```bash
# 1. Kiểm tra CHROMA_DB_PATH trong config.py:
CHROMA_DB_PATH = "./chroma_db"

# 2. Xóa & tạo mới:
# - Xóa thư mục chroma_db/
# - Chạy: python main.py

# 3. Kiểm tra quyền viết thư mục
```

---

## 5️⃣ LỖI SERVER FASTAPI

### ❌ `Address already in use` hoặc `Port 8000 already in use`

**Nguyên nhân**: Cổng 8000 đã bị chiếm bởi process khác

**Giải pháp**:

**Windows:**
```bash
# 1. Kiểm tra process chiếm cổng:
netstat -ano | findstr :8000

# 2. Dừng process (thay <PID> bằng số ID):
taskkill /PID <PID> /F

# 3. Hoặc đổi port trong config.py:
API_PORT = 8001  # hoặc 8002, 9000, ...
```

**macOS/Linux:**
```bash
# 1. Kiểm tra process chiếm cổng:
lsof -i :8000

# 2. Dừng process:
lsof -ti:8000 | xargs kill -9

# 3. Hoặc đổi port trong config.py:
API_PORT = 8001
```

---

### ❌ `Connection refused` khi truy cập http://localhost:8000

**Nguyên nhân**: Server chưa chạy hoặc chạy sai cổng

**Giải pháp**:

```bash
# 1. Kiểm tra server chạy chưa:
# - Xem có dòng "🎉 KHỞI ĐỘNG SERVER" không
# - Xem có "Uvicorn running on" không

# 2. Nếu chưa chạy:
python main.py

# 3. Kiểm tra cổng đúng:
# - Default: http://localhost:8000
# - Nếu đổi thành 8001: http://localhost:8001

# 4. Tạo virtual environment nếu cần:
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

## 6️⃣ LỖI KHI THÊM TÀI LIỆU

### ❌ `File not found` hoặc `No such file or directory`

**Nguyên nhân**: Đường dẫn file sai hoặc file không tồn tại

**Giải pháp**:

```bash
# 1. Kiểm tra đường dẫn file đúng:
# Sử dụng đường dẫn tuyệt đối: C:\Users\...\file.txt
# Hoặc đường dẫn tương đối: ./data/file.txt

# 2. Kiểm tra file tồn tại:
# Windows: dir C:\path\to\file.txt
# macOS/Linux: ls /path/to/file.txt

# 3. Upload file qua API:
curl -X POST http://localhost:8000/upload-file \
  -F "file=@/path/to/file.txt"
```

---

### ❌ `UnicodeDecodeError` khi đọc file

**Nguyên nhân**: File có encoding không phải UTF-8

**Giải pháp**:

```bash
# 1. Chuyển đổi encoding thành UTF-8:
# - Windows: Mở file với Notepad → Save As → UTF-8
# - macOS/Linux: iconv -f ISO-8859-1 -t UTF-8 input.txt > output.txt

# 2. Hoặc upload text trực tiếp qua API (không cần file)
```

---

## 7️⃣ LỖI EMBEDDING MODEL

### ❌ `Model download failed` hoặc `Connection timeout`

**Nguyên nhân**: Không thể tải model embedding từ Hugging Face

**Giải pháp**:

```bash
# 1. Tải model manual:
python -c "from sentence_transformers import SentenceTransformer; \
SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

# 2. Hoặc kiểm tra internet connection
# 3. Chờ đợi & thử lại

# 4. Nếu vẫn lỗi, dùng model khác:
# Trong config.py:
EMBEDDING_MODEL = "sentence-transformers/paraphrase-MiniLM-L6-v2"
```

---

### ❌ `OutOfMemory` hoặc `CUDA out of memory`

**Nguyên nhân**: RAM/GPU không đủ cho model embedding

**Giải pháp**:

```python
# 1. Sử dụng model nhỏ hơn trong config.py:
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# 2. Hoặc dùng CPU thay vì GPU:
# Trong rag_system.py:
self.embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={'device': 'cpu'}  # CPU thay vì cuda
)

# 3. Hoặc tăng RAM của server
```

---

## 8️⃣ LỖI LLM & GENERATION

### ❌ `Context length exceeded` hoặc `max_tokens too large`

**Nguyên nhân**: Tài liệu quá dài + prompt quá dài

**Giải pháp**:

```python
# Trong config.py:

# 1. Giảm LLM_MAX_TOKENS:
LLM_MAX_TOKENS = 512  # Thay vì 1024+

# 2. Giảm TOP_K_DOCUMENTS:
TOP_K_DOCUMENTS = 3  # Thay vì 5-10

# 3. Giảm CHUNK_SIZE:
CHUNK_SIZE = 300  # Thay vì 500+
```

---

### ❌ AI trả lời không liên quan hoặc sai

**Nguyên nhân**: Tài liệu không tốt, tham số không hợp lý

**Giải pháp**:

```python
# Trong config.py:

# 1. Tăng TOP_K_DOCUMENTS:
TOP_K_DOCUMENTS = 10  # Thay vì 5 (tìm kỹ hơn)

# 2. Giảm SIMILARITY_THRESHOLD:
SIMILARITY_THRESHOLD = 0.3  # Thay vì 0.5 (linh hoạt hơn)

# 3. Giảm LLM_TEMPERATURE:
LLM_TEMPERATURE = 0.3  # Thay vì 0.7 (chính xác hơn)

# 4. Sử dụng model embedding tốt hơn:
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"

# 5. Kiểm tra tài liệu:
# - Tài liệu có liên quan không?
# - Tài liệu có chính xác không?
# - CHUNK_SIZE phù hợp không?
```

---

## 9️⃣ LỖI TÓM LẠI & QUICK FIX

| Lỗi | Nguyên nhân | Fix nhanh |
|-----|-----------|----------|
| `ModuleNotFoundError` | Thư viện chưa cài | `pip install -r requirements.txt` |
| `OPENAI_API_KEY not found` | API key chưa set | `export OPENAI_API_KEY=sk-...` |
| `Port 8000 already in use` | Port bận | Sửa `API_PORT = 8001` |
| `Connection refused` | Server chưa chạy | `python main.py` |
| `chromadb locked` | Process khác dùng | Tắt server & xóa `chroma_db/` |
| `UnicodeDecodeError` | File encoding sai | Chuyển thành UTF-8 |
| `AI trả lời sai` | Tham số sai | Tăng `TOP_K_DOCUMENTS` |
| `Server chậm` | Quá nhiêu tài liệu | Giảm `CHUNK_SIZE`, `TOP_K` |

---

## 🆘 CẬP NHẬT LOG THÊM CHI TIẾT

Để xem log chi tiết, thay đổi trong `main.py`:

```python
uvicorn.run(
    "main:app",
    host=API_HOST,
    port=API_PORT,
    reload=API_RELOAD,
    log_level="debug"  # Thay "info" thành "debug"
)
```

---

**Nếu vẫn có vấn đề, vui lòng kiểm tra:**
1. Toàn bộ setup từ `QUICKSTART.md`
2. Console output (thường có hint chi tiết)
3. File `README.md` & `PARAMETERS.md`

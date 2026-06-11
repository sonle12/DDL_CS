# 🏗️ CẤU TRÚC TOÀN BỘ DỰ ÁN

---

## 📁 Cây Thư Mục

```
ai-chatbox-rag/
│
├── 📄 main.py                    # FastAPI Server (9 endpoints)
├── 📄 rag_system.py              # Logic RAG chính (chứa class RAGSystem)
├── 📄 config.py                  # Tất cả tham số cấu hình
├── 📄 demo.py                    # Script demo test hệ thống
│
├── 📄 requirements.txt           # Danh sách thư viện Python cần cài
├── 📄 .env.example              # Template file .env (API key)
│
├── 📁 chroma_db/                # Database vector (tự tạo lần đầu chạy)
│   └── (tệp database)
│
├── 📁 data/                      # Thư mục lưu tài liệu (tùy chọn)
│   └── (tài liệu .txt, .md, ...)
│
├── 📄 README.md                  # Hướng dẫn toàn bộ (tiếng Việt)
├── 📄 QUICKSTART.md              # Hướng dẫn nhanh (5 phút setup)
├── 📄 PARAMETERS.md              # Tất cả tham số + cách thay đổi
├── 📄 TROUBLESHOOTING.md         # Xử lý lỗi chi tiết
└── 📄 PROJECT_STRUCTURE.md       # File này (giải thích cấu trúc)
```

---

## 📋 Chi Tiết Các File

### 1. 🚀 `main.py` - FastAPI Server

**Chức năng**: HTTP API server để interact với RAG system

**Endpoints**:
```
GET  /                     # Test kết nối
GET  /health              # Kiểm tra trạng thái
POST /chat                # Chat (hỏi - đáp)
POST /add-documents       # Thêm tài liệu
POST /upload-file         # Upload file
POST /load-folder         # Tải folder tài liệu
GET  /history/{user_id}   # Lấy lịch sử chat
GET  /stats              # Thống kê hệ thống
DELETE /clear            # Xóa tất cả tài liệu
```

**Cấu trúc**:
```python
# 1. Định nghĩa Pydantic models (cấu trúc dữ liệu)
class ChatRequest(BaseModel): ...
class ChatResponse(BaseModel): ...

# 2. Khởi tạo FastAPI app
app = FastAPI(...)

# 3. Khởi tạo RAG System
rag_system = RAGSystem()

# 4. Định nghĩa endpoints
@app.post("/chat")
async def chat(request: ChatRequest): ...

# 5. Chạy uvicorn server
uvicorn.run()
```

**Cách sử dụng**:
```bash
python main.py
# Server chạy tại: http://localhost:8000
# API docs: http://localhost:8000/docs
```

---

### 2. 🧠 `rag_system.py` - Logic RAG Chính

**Chức năng**: Lớp RAGSystem quản lý toàn bộ logic

**Lớp chính**:
```python
class RAGSystem:
    def __init__(self)          # Khởi tạo embedding, ChromaDB, LLM
    def add_documents()         # Thêm tài liệu
    def query()                 # Hỏi câu hỏi (RAG retrieval + LLM)
    def _save_to_history()      # Lưu lịch sử
    def get_history()           # Lấy lịch sử chat
    def clear_documents()       # Xóa tất cả
    def get_stats()             # Lấy thống kê
```

**Quy trình RAG**:
```
Tài liệu
  ↓ (Chia nhỏ - Chunking)
Chunks [500 ký tự]
  ↓ (Tạo vector - Embedding)
Vectors [384 chiều]
  ↓ (Lưu trữ)
ChromaDB
  ↓
Câu hỏi → Embedding → Tìm kiếm tương tự → Lấy Top-5 tài liệu
                                          ↓
                                    LLM + Tài liệu → Phản hồi
                                          ↓
                                    Lưu lịch sử → ChromaDB
```

**Import**:
```python
from rag_system import RAGSystem, load_text_file, load_multiple_files
```

---

### 3. ⚙️ `config.py` - Tất Cả Tham Số

**Chức năng**: Quản lý tất cả tham số cấu hình

**Các nhóm tham số**:
```
1. EMBEDDING (Model chuyển text → vector)
2. CHROMA DB (Lưu trữ vector & lịch sử)
3. LLM (OpenAI - AI model)
4. RAG (Tìm kiếm tài liệu)
5. PROMPT (Hướng dẫn AI)
6. FASTAPI (Server)
7. LỊCH SỬ (Chat history)
```

**Cách sử dụng**:
```python
# main.py, rag_system.py tự động import:
from config import TOP_K_DOCUMENTS, LLM_TEMPERATURE, ...

# Để thay đổi: Sửa trực tiếp trong config.py
TOP_K_DOCUMENTS = 10  # Thay từ 5 → 10
```

**Ví dụ quan trọng**:
```python
# Để AI thông minh hơn:
LLM_MODEL_NAME = "gpt-4"           # Model tốt nhất
TOP_K_DOCUMENTS = 10                # Tìm kỹ hơn
SIMILARITY_THRESHOLD = 0.3          # Linh hoạt hơn
```

---

### 4. 🎮 `demo.py` - Script Demo

**Chức năng**: Test hệ thống RAG hoạt động đúng không

**Các bước**:
```
1. Khởi tạo RAG System
2. Thêm tài liệu mẫu
3. Hiển thị thống kê
4. Test chat với 3 câu hỏi
5. Hiển thị lịch sử
```

**Cách sử dụng**:
```bash
python demo.py
# Kết quả: "🎉 DEMO HOÀN THÀNH!"
```

**Khi nào chạy**:
- Sau khi cài đặt xong
- Kiểm tra hệ thống có lỗi không
- Học cách sử dụng RAGSystem

---

### 5. 📦 `requirements.txt` - Danh Sách Thư Viện

**Chức năng**: Liệt kê tất cả thư viện Python cần cài

**Nội dung**:
```
fastapi==0.104.1              # Web framework
uvicorn==0.24.0               # ASGI server
langchain==0.1.0              # LLM framework
langchain-community==0.0.10   # LangChain community
chromadb==0.4.17              # Vector database
openai==1.3.0                 # OpenAI API
python-dotenv==1.0.0          # .env support
pydantic==2.5.0               # Data validation
sentence-transformers==2.2.2  # Embedding model
numpy==1.24.3                 # Numerical computing
```

**Cách sử dụng**:
```bash
pip install -r requirements.txt
```

---

### 6. 🔑 `.env.example` - Template API Key

**Chức năng**: Template để tạo file `.env` (lưu API key an toàn)

**Cách sử dụng**:
```bash
# 1. Copy file
cp .env.example .env

# 2. Sửa trong .env
OPENAI_API_KEY=sk-your-actual-key

# 3. Python sẽ tự động load từ .env
# (Không cần set environment variable)
```

---

### 7. 📁 `chroma_db/` - Database Vector

**Chức năng**: Lưu trữ:
- Vector embeddings (chuyển đổi text)
- Lịch sử chat
- Metadata của tài liệu

**Cấu trúc**:
```
chroma_db/
├── (binary files)  # Dữ liệu vector
└── (được quản lý tự động bởi ChromaDB)
```

**Cách quản lý**:
```bash
# Xóa database (nuôi lại từ đầu):
rm -r chroma_db/  # macOS/Linux
rmdir /s chroma_db  # Windows

# Server sẽ tự tạo mới khi khởi động
```

---

### 8. 📁 `data/` - Thư Mục Tài Liệu

**Chức năng**: Lưu các tài liệu cần upload

**Cách sử dụng**:
```bash
# 1. Đặt file vào thư mục này
data/
├── company.txt
├── products.md
└── news.txt

# 2. Upload qua API:
curl -X POST http://localhost:8000/load-folder \
  -d "folder_path=./data" \
  -d "file_pattern=*.txt"
```

---

### 9. 📖 `README.md` - Hướng Dẫn Toàn Bộ

**Chức năng**: Tài liệu hướng dẫn chi tiết (tiếng Việt)

**Nội dung**:
```
1. Giới thiệu
2. Kiến trúc hệ thống
3. Cài đặt
4. Cách sử dụng
5. API Endpoints
6. Danh sách tham số & tối ưu
7. Ví dụ sử dụng
8. Troubleshooting
```

**Khi nào đọc**: Lần đầu setup hoặc cần hiểu chi tiết

---

### 10. ⚡ `QUICKSTART.md` - Hướng Dẫn Nhanh

**Chức năng**: Setup trong 5 phút

**Nội dung**:
```
Bước 1: Cài Python (5 phút)
Bước 2: Cài thư viện (3-5 phút)
Bước 3: Lấy OpenAI API key (2 phút)
Bước 4: Chạy demo (2 phút)
Bước 5: Chạy server (30 giây)
Bước 6: Test API (thực hành)
```

**Khi nào đọc**: Lần đầu setup, muốn nhanh

---

### 11. 🎯 `PARAMETERS.md` - Tất Cả Tham Số

**Chức năng**: Liệt kê tất cả tham số + cách thay đổi

**Nội dung**:
```
1. Hướng chuyên mục (muốn AI thông minh → làm gì)
2. Bảng tất cả tham số
3. Cách sửa đổi tham số
4. Bảng so sánh scenarios
5. FAQ
```

**Khi nào đọc**: Muốn tối ưu AI, thay đổi tham số

---

### 12. 🆘 `TROUBLESHOOTING.md` - Xử Lý Lỗi

**Chức năng**: Giải pháp cho tất cả lỗi thường gặp

**Nội dung**:
```
1. Lỗi cài đặt Python/pip
2. Lỗi cài thư viện
3. Lỗi OpenAI API
4. Lỗi ChromaDB
5. Lỗi FastAPI server
6. Lỗi thêm tài liệu
7. Lỗi embedding model
8. Lỗi LLM & generation
9. Bảng tóm lược lỗi
```

**Khi nào đọc**: Khi gặp lỗi

---

## 🔄 Quy Trình Hoạt Động Toàn Bộ

### Khởi Động Lần Đầu

```
1. Chạy: python main.py
   ↓
2. main.py import config → RAGSystem
   ↓
3. RAGSystem.__init__():
   - Load embedding model (22MB, ~30 giây)
   - Khởi tạo ChromaDB
   - Khởi tạo OpenAI LLM
   - Tạo RAG chain
   ↓
4. FastAPI server chạy tại :8000
   ↓
5. Sẵn sàng nhận API requests
```

### Thêm Tài Liệu

```
1. User gửi POST /add-documents
   ↓
2. main.py gọi: rag_system.add_documents()
   ↓
3. rag_system.py:
   - Chia tài liệu thành chunks
   - Tạo embedding cho mỗi chunk
   - Lưu vào ChromaDB
   ↓
4. Trả về thành công
```

### Chat (Hỏi - Đáp)

```
1. User gửi POST /chat + câu hỏi
   ↓
2. main.py gọi: rag_system.query()
   ↓
3. rag_system.py:
   a) Embedding câu hỏi
   b) Tìm kiếm tương tự từ ChromaDB (Top-5)
   c) Lọc theo SIMILARITY_THRESHOLD
   d) Gắn tài liệu + câu hỏi → LLM
   e) LLM sinh phản hồi
   f) Lưu lịch sử vào ChromaDB
   ↓
4. Trả về phản hồi + tài liệu liên quan
```

---

## 📊 Mối Liên Hệ Giữa Các File

```
┌─────────────────────────────────────────┐
│            main.py                      │
│         (FastAPI Server)                │
│  - Định nghĩa 9 endpoints               │
│  - Xử lý HTTP requests                  │
└──────────────┬──────────────────────────┘
               │ import
               ↓
┌─────────────────────────────────────────┐
│         rag_system.py                   │
│      (Logic RAG chính)                  │
│  - Class RAGSystem                      │
│  - Embedding → ChromaDB → LLM           │
└──────────────┬──────────────────────────┘
               │ import
               ↓
┌─────────────────────────────────────────┐
│           config.py                     │
│      (Tất cả tham số)                   │
│  - TOP_K_DOCUMENTS = 5                  │
│  - LLM_TEMPERATURE = 0.7                │
│  - ...                                  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│         External Services               │
│  - OpenAI API (LLM)                     │
│  - Hugging Face (Embedding model)       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│          ChromaDB                       │
│    (Vector Store & History)             │
│  - Lưu embeddings                       │
│  - Lưu lịch sử chat                     │
└─────────────────────────────────────────┘
```

---

## 🎯 Sơ Đồ Dữ Liệu

```
FLOW:
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Documents│────▶│ Chunks   │────▶│ Vectors  │────▶│ChromaDB  │
└──────────┘     └──────────┘     │(384-D)  │     └──────────┘
                                  └──────────┘

QUERY:
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Question │────▶│ Vector   │────▶│ Search   │────▶│Top-5     │
└──────────┘     │(384-D)  │     │(Semantic)│     │Docs      │
                 └──────────┘     └──────────┘     └──────────┘
                                                          │
                                                          ↓
                                                   ┌──────────┐
                                                   │LLM       │
                                                   │(GPT-3.5) │
                                                   └────┬─────┘
                                                        │
                                                        ↓
                                                   ┌──────────┐
                                                   │Response  │
                                                   └──────────┘
```

---

## 📈 Độ Quan Trọng Các File

| File | Tầm quan trọng | Khi nào chỉnh sửa |
|------|----------------|------------------|
| `config.py` | 🔥🔥🔥 Cực cao | Tối ưu tham số |
| `main.py` | 🔥🔥 Cao | Thêm endpoints |
| `rag_system.py` | 🔥 Trung bình | Fine-tune logic RAG |
| `demo.py` | ⭐ Thấp | Test thôi |
| `README.md` | ⭐ Thấp | Reference |

---

## 💾 Dung Lượng Ước Tính

| Thành phần | Dung lượng |
|-----------|-----------|
| Python 3.x | ~100MB |
| Thư viện (pip) | ~800MB |
| Embedding model | ~22-438MB |
| ChromaDB (1000 tài liệu) | ~50-200MB |
| **Tổng cộng** | **~1-1.5GB** |

---

**Chúc bạn sử dụng thành công! 🎉**

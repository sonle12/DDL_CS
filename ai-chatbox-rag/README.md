# 🤖 Hệ Thống AI Chatbox Với RAG, LangChain, ChromaDB & FastAPI

## 📖 Mục Lục
1. [Giới thiệu](#giới-thiệu)
2. [Kiến trúc hệ thống](#kiến-trúc-hệ-thống)
3. [Cài đặt](#cài-đặt)
4. [Cách sử dụng](#cách-sử-dụng)
5. [API Endpoints](#api-endpoints)
6. [Danh sách tham số & Cách tối ưu](#danh-sách-tham-số--cách-tối-ưu)
7. [Ví dụ sử dụng](#ví-dụ-sử-dụng)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Giới Thiệu

Đây là một hệ thống **AI Chatbox hiện đại** sử dụng **RAG (Retrieval-Augmented Generation)** để trả lời câu hỏi dựa trên tài liệu được cung cấp.

### 🔑 Công nghệ sử dụng:

- **RAG (Retrieval-Augmented Generation)**: Kết hợp tìm kiếm tài liệu + sinh phản hồi AI
- **LangChain**: Framework tích hợp LLM + vector store
- **ChromaDB**: Database vector lưu trữ embeddings & lịch sử chat
- **OpenAI GPT**: Large Language Model (LLM) để sinh phản hồi
- **Sentence Transformers**: Embedding model chuyển văn bản thành vector
- **FastAPI**: API server hiệu năng cao

### 📊 Quy trình hoạt động:

```
Tài liệu → Chia nhỏ (Chunking) → Embedding → ChromaDB (Vector Store)
                                              ↓
Câu hỏi → Embedding → Tìm kiếm tương tự → Lấy tài liệu liên quan
                                           ↓
                                   LLM + Tài liệu → Sinh phản hồi
                                           ↓
                                    Lưu lịch sử → ChromaDB
```

---

## 🏗️ Kiến Trúc Hệ Thống

```
ai-chatbox-rag/
├── main.py                 # FastAPI server (8 endpoints)
├── rag_system.py           # Logic hệ thống RAG chính
├── config.py               # Tất cả tham số có thể cấu hình
├── requirements.txt        # Danh sách thư viện Python
├── chroma_db/              # Database (tự tạo sau lần chạy đầu)
│   └── (vector embeddings & lịch sử)
├── data/                   # Thư mục chứa tài liệu gốc (tùy chọn)
└── README.md              # Hướng dẫn này

```

### 📦 Thành phần chính:

| File | Chức năng |
|------|----------|
| `main.py` | FastAPI server với 9 endpoints |
| `rag_system.py` | Lớp RAGSystem quản lý embedding, retrieval, chat |
| `config.py` | **Tất cả tham số có thể tuỳ chỉnh** |
| `requirements.txt` | Thư viện cần cài đặt |

---

## 🚀 Cài Đặt

### Yêu cầu:
- Python 3.8+
- pip (package manager)
- OpenAI API key

### Bước 1: Clone/Download dự án

```bash
cd ai-chatbox-rag
```

### Bước 2: Tạo virtual environment (khuyến nghị)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Bước 4: Thiết lập OpenAI API Key

**Cách 1: Environment variable (khuyến nghị)**
```bash
# Windows PowerShell
$env:OPENAI_API_KEY = "sk-your-api-key-here"

# Windows CMD
set OPENAI_API_KEY=sk-your-api-key-here

# macOS/Linux
export OPENAI_API_KEY="sk-your-api-key-here"
```

**Cách 2: Chỉnh trực tiếp trong `config.py`** (không an toàn)
```python
OPENAI_API_KEY = "sk-your-api-key-here"
```

### Bước 5: Chạy server

```bash
python main.py
```

✅ **Kết quả**:
```
================================================================================
🎉 KHỞI ĐỘNG SERVER
================================================================================
🌐 Server sẽ chạy tại: http://0.0.0.0:8000
📚 API Documentation: http://localhost:8000/docs
🔄 OpenAPI Schema: http://localhost:8000/openapi.json
================================================================================
```

Truy cập: **http://localhost:8000/docs** để xem API interactive

---

## 💬 Cách Sử Dụng

### 1️⃣ Thêm Tài Liệu

#### Cách A: Thêm text trực tiếp

```bash
curl -X POST http://localhost:8000/add-documents \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      "Công ty X được thành lập năm 2020. Công ty có 500 nhân viên.",
      "Sản phẩm chính là phần mềm quản lý doanh nghiệp."
    ],
    "metadata": [
      {"source": "company_info.txt"},
      {"source": "products.txt"}
    ]
  }'
```

#### Cách B: Upload file

```bash
curl -X POST http://localhost:8000/upload-file \
  -F "file=@/path/to/document.txt"
```

#### Cách C: Tải folder

```bash
curl -X POST http://localhost:8000/load-folder \
  -d "folder_path=/path/to/documents" \
  -d "file_pattern=*.txt"
```

### 2️⃣ Chat (Hỏi - Đáp)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Công ty X có bao nhiêu nhân viên?",
    "user_id": "user_123"
  }'
```

**Phản hồi**:
```json
{
  "question": "Công ty X có bao nhiêu nhân viên?",
  "answer": "Theo tài liệu, Công ty X có 500 nhân viên.",
  "relevant_documents": [
    {
      "content": "Công ty X được thành lập năm 2020. Công ty có 500 nhân viên.",
      "similarity": 0.92,
      "metadata": {"source": "company_info.txt"}
    }
  ],
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### 3️⃣ Xem Lịch Sử Chat

```bash
curl http://localhost:8000/history/user_123
```

### 4️⃣ Xem Thống Kê Hệ Thống

```bash
curl http://localhost:8000/stats
```

---

## 🔌 API Endpoints

| Endpoint | Method | Mô Tả |
|----------|--------|-------|
| `/` | GET | Test kết nối |
| `/health` | GET | Kiểm tra trạng thái |
| `/chat` | POST | **Gửi câu hỏi & nhận phản hồi** |
| `/add-documents` | POST | Thêm tài liệu (text) |
| `/upload-file` | POST | Upload file (.txt, .md) |
| `/load-folder` | POST | Tải folder tài liệu |
| `/history/{user_id}` | GET | Lấy lịch sử chat |
| `/stats` | GET | Thống kê hệ thống |
| `/clear` | DELETE | Xóa tất cả tài liệu ⚠️ |

---

## 📊 Danh Sách Tham Số & Cách Tối Ưu

> **📌 CHÚ Ý**: Mở file `config.py` để tìm và chỉnh các tham số này

### 🎯 NHÓM 1: EMBEDDING MODEL (Chuyển văn bản thành vector)

**Tham số**: `EMBEDDING_MODEL` (config.py, dòng ~19)

```python
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
```

| Model | Kích thước | Tốc độ | Chất lượng | Khuyến nghị |
|-------|-----------|--------|-----------|-------------|
| `all-MiniLM-L6-v2` | 22MB | ⚡⚡⚡ | ⭐⭐⭐ | ✅ **Khuyến nghị** |
| `all-mpnet-base-v2` | 438MB | ⚡ | ⭐⭐⭐⭐⭐ | 🔧 Cao cấp |
| `paraphrase-multilingual-mpnet-base-v2` | 438MB | ⚡ | ⭐⭐⭐⭐ | 🇻🇳 Đa ngôn ngữ |

**🚀 Tối ưu hóa**:
- ✅ Để nhanh & nhẹ: Giữ `all-MiniLM-L6-v2`
- 🔧 Để chất lượng tốt hơn: Đổi thành `all-mpnet-base-v2` (chậm hơn)
- 🇻🇳 Để hỗ trợ Tiếng Việt tốt: Đổi thành `paraphrase-multilingual-mpnet-base-v2`

---

### 🎯 NHÓM 2: RAG RETRIEVAL (Tìm kiếm tài liệu)

#### 1. `TOP_K_DOCUMENTS` (config.py, dòng ~52)

```python
TOP_K_DOCUMENTS = 5  # Số tài liệu lấy ra
```

| Giá trị | Tốc độ | Chất lượng | Khi nào dùng |
|--------|--------|-----------|-------------|
| 3 | ⚡⚡⚡ | ⭐⭐ | 💰 Rẻ, nhanh (API cost thấp) |
| 5 | ⚡⚡ | ⭐⭐⭐ | ✅ **Khuyến nghị** (balance) |
| 10 | ⚡ | ⭐⭐⭐⭐ | 🔍 Tìm kiếm kỹ lưỡng |
| 20 | 🐢 | ⭐⭐⭐⭐⭐ | 📚 Tài liệu lớn, phức tạp |

**💡 Công thức**: `TOP_K_DOCUMENTS = số_tài_liệu_liên_quan_tối_đa`

**🚀 Tối ưu hóa**:
- Muốn AI **chính xác hơn**: Tăng từ 5 → 10
- Muốn **nhanh hơn & rẻ hơn**: Giảm từ 5 → 3
- Tài liệu **phức tạp**: Tăng lên 15-20

---

#### 2. `SIMILARITY_THRESHOLD` (config.py, dòng ~55)

```python
SIMILARITY_THRESHOLD = 0.5  # Ngưỡng độ tương tự (0-1)
```

| Giá trị | Ý nghĩa | Khi nào dùng |
|--------|---------|-------------|
| 0.3 | Linh hoạt, chấp nhận nhiều | 🤖 AI sáng tạo, tổng hợp |
| 0.5 | Cân bằng | ✅ **Khuyến nghị** |
| 0.7 | Nghiêm ngặt, chỉ chính xác | 📋 Tài liệu kỹ thuật, pháp lý |
| 0.8+ | Cực kỳ nghiêm ngặt | 🔒 An toàn, y tế |

**🚀 Tối ưu hóa**:
- Muốn AI **chỉ trả lời khi chắc chắn**: Tăng thành 0.7 - 0.8
- Muốn AI **linh hoạt, sáng tạo**: Giảm thành 0.3 - 0.4
- Tài liệu **chuyên môn (Y tế, Pháp lý)**: Đặt 0.75 - 0.85

---

#### 3. `CHUNK_SIZE` (config.py, dòng ~59)

```python
CHUNK_SIZE = 500  # Kích thước mỗi đoạn (ký tự)
```

| Giá trị | Đặc điểm | Khi nào dùng |
|--------|----------|-------------|
| 300 | ✂️ Cắt nhỏ, chi tiết | 📄 Tài liệu đơn giản, short |
| 500 | ⚖️ Cân bằng | ✅ **Khuyến nghị** |
| 800 | 📖 Lớn, ngữ cảnh dày đặc | 📚 Tài liệu dài, phức tạp |
| 1500 | 🏢 Rất lớn | 📊 Dữ liệu lớn, nhiều ngữ cảnh |

**🚀 Tối ưu hóa**:
- Tài liệu đơn giản (tiểu sử): Đặt 300-400
- Tài liệu vừa (tin tức, blog): Giữ 500
- Tài liệu phức tạp (sách, paper): Tăng 800-1000

---

#### 4. `CHUNK_OVERLAP` (config.py, dòng ~64)

```python
CHUNK_OVERLAP = 100  # Độ trùng lặp giữa chunks
```

**Công thức khuyến nghị**: `CHUNK_OVERLAP ≈ CHUNK_SIZE / 5`

| Giá trị | Ngữ cảnh | Khi nào dùng |
|--------|----------|-------------|
| 0 | Không trùng | ⚡ Nhanh, nhưng mất ngữ cảnh |
| 50 | Ít trùng | 💨 Cân bằng tốc độ |
| 100 | Trùng vừa phải | ✅ **Khuyến nghị** |
| 200+ | Trùng nhiều | 🧠 Giữ ngữ cảnh tốt (chậm hơn) |

**🚀 Tối ưu hóa**:
- Muốn **nhanh**: Giảm thành 30-50
- Muốn **ngữ cảnh tốt**: Tăng thành 150-200

---

### 🎯 NHÓM 3: LLM (Language Model - AI)

#### 1. `LLM_MODEL_NAME` (config.py, dòng ~39)

```python
LLM_MODEL_NAME = "gpt-3.5-turbo"
```

| Model | Tốc độ | Thông minh | Chi phí | Khuyến nghị |
|-------|--------|-----------|--------|-------------|
| `gpt-3.5-turbo` | ⚡⚡⚡ | ⭐⭐⭐ | 💵 | ✅ **Khuyến nghị** |
| `gpt-4-turbo-preview` | ⚡⚡ | ⭐⭐⭐⭐⭐ | 💵💵 | 🔧 Cao cấp |
| `gpt-4` | ⚡ | ⭐⭐⭐⭐⭐ | 💵💵💵 | 🏆 Tốt nhất |

**🚀 Tối ưu hóa**:
- Muốn **rẻ & nhanh**: Giữ `gpt-3.5-turbo`
- Muốn **thông minh hơn**: Đổi thành `gpt-4-turbo-preview`
- Muốn **tốt nhất**: Đổi thành `gpt-4`

---

#### 2. `LLM_TEMPERATURE` (config.py, dòng ~46)

```python
LLM_TEMPERATURE = 0.7  # Độ sáng tạo (0-1)
```

| Giá trị | Ý nghĩa | Khi nào dùng |
|--------|---------|-------------|
| 0.0 | Chính xác, nhất quán | 📋 QA kỹ thuật, pháp lý |
| 0.3 | Chính xác, ít sáng tạo | ✅ **Khuyến nghị** |
| 0.7 | Cân bằng | ⚖️ Hỏi-đáp thông thường |
| 0.9 | Sáng tạo, đa dạng | 🎨 Brainstorm, sáng tác |
| 1.0 | Cực kỳ ngẫu nhiên | 🎮 Game, trò chơi |

**🚀 Tối ưu hóa**:
- Muốn phản hồi **chính xác, nhất quán**: Đặt 0.2 - 0.3
- Muốn **phản hồi đa dạng, sáng tạo**: Đặt 0.8 - 0.9

---

#### 3. `LLM_MAX_TOKENS` (config.py, dòng ~49)

```python
LLM_MAX_TOKENS = 1024  # Độ dài tối đa phản hồi
```

| Giá trị | Độ dài | Chi phí | Khi nào dùng |
|--------|--------|--------|-------------|
| 256 | 🐜 Rất ngắn | 💵 | ⚡ Nhanh, rẻ (câu trả lời ngắn) |
| 512 | 📝 Ngắn | 💵 | 💨 Câu trả lời vừa |
| 1024 | 📄 Vừa | 💵💵 | ✅ **Khuyến nghị** |
| 2048 | 📖 Dài | 💵💵💵 | 📚 Câu trả lời chi tiết |
| 4096 | 📕 Rất dài | 💵💵💵💵 | 🎓 Hỏi-đáp phức tạp |

**🚀 Tối ưu hóa**:
- Muốn **nhanh & rẻ**: Giảm thành 256-512
- Muốn **chi tiết**: Tăng thành 2048-4096

---

### 🎯 NHÓM 4: SERVER (FastAPI)

#### 1. `API_PORT` (config.py, dòng ~74)

```python
API_PORT = 8000  # Cổng chạy server
```

**🚀 Tối ưu hóa**:
- Cổng 8000 bị chiếm: Đổi thành 8001, 8002, 9000
- Chạy trên server: Có thể sử dụng cổng 80 (HTTP) hoặc 443 (HTTPS)

---

#### 2. `API_RELOAD` (config.py, dòng ~77)

```python
API_RELOAD = True  # Tự động reload khi code thay đổi
```

**🚀 Tối ưu hóa**:
- **Dev mode** (phát triển): Giữ `True` (tự động reload)
- **Production** (chạy thực): Đổi thành `False` (ổn định)

---

### 🎯 NHÓM 5: LỊCH SỬ CHAT

#### `MAX_HISTORY_MESSAGES` (config.py, dòng ~87)

```python
MAX_HISTORY_MESSAGES = 20  # Số tin nhắn lịch sử lưu
```

| Giá trị | Bộ nhớ | Khi nào dùng |
|--------|--------|-------------|
| 5 | 🔋 Rất nhẹ | ⚡ Tiết kiệm tài nguyên |
| 10 | 🔋 Nhẹ | 💨 Giới hạn tài nguyên |
| 20 | ⚖️ Cân bằng | ✅ **Khuyến nghị** |
| 50 | 📦 Nặng | 🧠 Nhớ lâu hơn |
| 100+ | 📦 Rất nặng | 💾 Server có RAM cao |

**🚀 Tối ưu hóa**:
- Muốn **AI nhớ lâu hơn**: Tăng thành 50-100
- Muốn **tiết kiệm tài nguyên**: Giảm thành 5-10

---

### 🎯 NHÓM 6: PROMPT HỆ THỐNG

#### `SYSTEM_PROMPT` (config.py, dòng ~82)

```python
SYSTEM_PROMPT = """Bạn là một trợ lý AI thông minh...
"""
```

**🚀 Tối ưu hóa**:
- Muốn AI **chuyên môn hơn**: Thêm chỉ dẫn cụ thể
  ```
  "Bạn là một chuyên gia Y tế. Trả lời các câu hỏi về sức khỏe..."
  ```
- Muốn AI **thân thiện hơn**: Thêm tính cách
  ```
  "Bạn là một người bạn thân thiện. Luôn tỏ ra quan tâm..."
  ```

---

## 🎓 Ví Dụ Sử Dụng

### Ví dụ 1: AI Chatbox Về Công Ty

#### Bước 1: Chuẩn bị tài liệu

Tạo file `company_data.txt`:
```
Công ty X được thành lập năm 2020 bởi các nhà sáng lập công nghệ.
Công ty X hiện có 500 nhân viên tại Hà Nội, Hồ Chí Minh và Đà Nẵng.
Sản phẩm chính là phần mềm quản lý doanh nghiệp cho các SME.
Công ty X đã nhận được tài trợ từ các nhà đầu tư hàng đầu.
```

#### Bước 2: Upload tài liệu

```bash
curl -X POST http://localhost:8000/upload-file \
  -F "file=@company_data.txt"
```

#### Bước 3: Chat

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Công ty X có bao nhiêu nhân viên?",
    "user_id": "user_1"
  }'
```

**Phản hồi**:
```json
{
  "question": "Công ty X có bao nhiêu nhân viên?",
  "answer": "Công ty X hiện có 500 nhân viên tại Hà Nội, Hồ Chí Minh và Đà Nẵng.",
  "relevant_documents": [...],
  "timestamp": "2024-01-15T10:30:45"
}
```

### Ví dụ 2: Tối ưu AI Để Chính Xác Hơn

**Chỉnh trong `config.py`**:
```python
# Mục tiêu: AI chính xác, không sáng tạo
LLM_TEMPERATURE = 0.3  # Giảm từ 0.7 (ít sáng tạo)
TOP_K_DOCUMENTS = 10   # Tăng từ 5 (tìm kiếm kỹ)
SIMILARITY_THRESHOLD = 0.7  # Tăng từ 0.5 (nghiêm ngặt)
LLM_MAX_TOKENS = 512   # Giảm để phản hồi ngắn gọn
```

### Ví dụ 3: AI Chatbox Nhanh & Rẻ

**Chỉnh trong `config.py`**:
```python
# Mục tiêu: Nhanh, tiết kiệm API cost
LLM_MODEL_NAME = "gpt-3.5-turbo"  # Model rẻ
TOP_K_DOCUMENTS = 3  # Ít tài liệu → nhanh hơn
LLM_MAX_TOKENS = 256  # Phản hồi ngắn
LLM_TEMPERATURE = 0.9  # Không cần sáng tạo
```

---

## 🔧 Troubleshooting

### ❌ Lỗi: `OPENAI_API_KEY not found`

**Giải pháp**:
1. Kiểm tra API key có đúng: Truy cập https://platform.openai.com/account/api-keys
2. Thiết lập environment variable:
   ```bash
   export OPENAI_API_KEY="sk-..."  # macOS/Linux
   # hoặc
   $env:OPENAI_API_KEY = "sk-..."  # Windows PowerShell
   ```
3. Kiểm tra lại `.env` file (nếu có)

---

### ❌ Lỗi: `ChromaDB connection failed`

**Giải pháp**:
1. Kiểm tra thư mục `chroma_db` có tồn tại
2. Xóa thư mục `chroma_db` và khởi động lại server (sẽ tạo mới)
3. Kiểm tra quyền viết file của folder

---

### ❌ Lỗi: `Port 8000 already in use`

**Giải pháp**:
1. Thay đổi port trong `config.py`:
   ```python
   API_PORT = 8001  # hoặc số cổng khác
   ```
2. Hoặc dừng process chiếm cổng 8000:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   
   # macOS/Linux
   lsof -ti:8000 | xargs kill -9
   ```

---

### ⚠️ Cảnh báo: AI trả lời sai/không liên quan

**Giải pháp**:
1. Kiểm tra tài liệu được upload: `/stats`
2. Tăng `TOP_K_DOCUMENTS`: 5 → 10
3. Giảm `SIMILARITY_THRESHOLD`: 0.5 → 0.3
4. Chọn embedding model tốt hơn: `all-mpnet-base-v2`
5. Chỉnh `CHUNK_SIZE` để phù hợp với tài liệu

---

### ⚠️ Cảnh báo: Server chậm

**Giải pháp**:
1. Giảm `TOP_K_DOCUMENTS`: 10 → 5 → 3
2. Giảm `CHUNK_SIZE`: 800 → 500 → 300
3. Sử dụng model nhẹ hơn: `all-MiniLM-L6-v2`
4. Giảm `LLM_MAX_TOKENS`: 1024 → 512

---

### ❌ Lỗi: `Embedding model download failed`

**Giải pháp**:
```bash
# Tải model manually
python -c "from sentence_transformers import SentenceTransformer; \
SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```

---

## 📚 Tài liệu Tham Khảo

- **LangChain**: https://python.langchain.com/
- **ChromaDB**: https://www.trychroma.com/
- **OpenAI API**: https://platform.openai.com/docs
- **FastAPI**: https://fastapi.tiangolo.com/
- **Sentence Transformers**: https://www.sbert.net/

---

## 📋 Danh Sách Tham Số - TÓM LƯỢC (THAY ĐỔI Ở `config.py`)

### 🔥 THAM SỐ QUAN TRỌNG NHẤT

| Tham số | Giá trị mặc định | Thay đổi khi | Ảnh hưởng |
|---------|-----------------|-------------|----------|
| `LLM_MODEL_NAME` | gpt-3.5-turbo | Muốn thông minh hơn → gpt-4 | 🧠 Chất lượng AI |
| `TOP_K_DOCUMENTS` | 5 | Muốn chính xác hơn → 10 | 🎯 Độ chính xác |
| `SIMILARITY_THRESHOLD` | 0.5 | Muốn nghiêm ngặt hơn → 0.7 | ✓ Độ tin cậy |
| `LLM_TEMPERATURE` | 0.7 | Muốn chính xác hơn → 0.3 | 🎲 Độ sáng tạo |
| `EMBEDDING_MODEL` | all-MiniLM-L6-v2 | Muốn tốt hơn → all-mpnet-base-v2 | 🔍 Chất lượng tìm kiếm |

### 📊 BẢNG TỐI ƯU HÓA NHANH

**Để AI THÔNG MINH HƠN:**
```python
LLM_MODEL_NAME = "gpt-4"  # Hoặc gpt-4-turbo-preview
TOP_K_DOCUMENTS = 10       # Tăng từ 5
SIMILARITY_THRESHOLD = 0.3 # Giảm từ 0.5
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
```

**Để NHANH HƠN & RẺ HƠN:**
```python
LLM_MODEL_NAME = "gpt-3.5-turbo"
TOP_K_DOCUMENTS = 3        # Giảm từ 5
LLM_MAX_TOKENS = 256       # Giảm từ 1024
CHUNK_SIZE = 300           # Giảm từ 500
```

**Để CHÍNH XÁC HƠN:**
```python
LLM_TEMPERATURE = 0.3      # Giảm từ 0.7
SIMILARITY_THRESHOLD = 0.8 # Tăng từ 0.5
TOP_K_DOCUMENTS = 15       # Tăng từ 5
```

**Để AI NHỚ LÂUHƠN:**
```python
MAX_HISTORY_MESSAGES = 100 # Tăng từ 20
```

---

## 📞 Liên Hệ & Hỗ Trợ

Nếu có vấn đề:
1. Kiểm tra console output (thường có hint)
2. Xem phần **Troubleshooting** ở trên
3. Đọc log chi tiết (chỉnh `log_level` trong `main.py`)

---

**🎉 Chúc bạn sử dụng hệ thống thành công!**

*Cập nhật: 2024*

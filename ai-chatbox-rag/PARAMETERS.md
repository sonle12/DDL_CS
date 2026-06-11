# 📋 DANH SÁCH TẤT CẢ THAM SỐ & CÁCH THAY ĐỔI

> **QUAN TRỌNG**: Tất cả tham số nằm trong file `config.py`
> Mở `config.py` và tìm tên tham số dưới đây để chỉnh sửa

---

## 🎯 HƯỚNG CHUYÊN MỤC

### 🚀 Muốn AI Thông Minh Hơn?

1. **Mở `config.py`** tìm:
   ```python
   LLM_MODEL_NAME = "gpt-3.5-turbo"
   ```
   **Đổi thành:**
   ```python
   LLM_MODEL_NAME = "gpt-4"
   ```

2. **Tìm:**
   ```python
   TOP_K_DOCUMENTS = 5
   ```
   **Đổi thành:**
   ```python
   TOP_K_DOCUMENTS = 10
   ```

3. **Tìm:**
   ```python
   SIMILARITY_THRESHOLD = 0.5
   ```
   **Đổi thành:**
   ```python
   SIMILARITY_THRESHOLD = 0.3
   ```

4. **Tìm:**
   ```python
   EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
   ```
   **Đổi thành:**
   ```python
   EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
   ```

---

### ⚡ Muốn Nhanh Hơn & Rẻ Hơn?

1. **Tìm:**
   ```python
   TOP_K_DOCUMENTS = 5
   ```
   **Đổi thành:**
   ```python
   TOP_K_DOCUMENTS = 3
   ```

2. **Tìm:**
   ```python
   LLM_MAX_TOKENS = 1024
   ```
   **Đổi thành:**
   ```python
   LLM_MAX_TOKENS = 256
   ```

3. **Tìm:**
   ```python
   CHUNK_SIZE = 500
   ```
   **Đổi thành:**
   ```python
   CHUNK_SIZE = 300
   ```

---

### 🧠 Muốn AI Chính Xác Hơn?

1. **Tìm:**
   ```python
   LLM_TEMPERATURE = 0.7
   ```
   **Đổi thành:**
   ```python
   LLM_TEMPERATURE = 0.3
   ```

2. **Tìm:**
   ```python
   SIMILARITY_THRESHOLD = 0.5
   ```
   **Đổi thành:**
   ```python
   SIMILARITY_THRESHOLD = 0.8
   ```

3. **Tìm:**
   ```python
   TOP_K_DOCUMENTS = 5
   ```
   **Đổi thành:**
   ```python
   TOP_K_DOCUMENTS = 15
   ```

---

### 🧠 Muốn AI Nhớ Lâu Hơn?

**Tìm:**
```python
MAX_HISTORY_MESSAGES = 20
```

**Đổi thành:**
```python
MAX_HISTORY_MESSAGES = 100
```

---

## 📊 BẢNG TẤT CẢ THAM SỐ

### 1. EMBEDDING MODEL (Chuyển văn bản → Vector)

| Tham số | Tệp | Dòng | Giá trị mặc định | Giải thích |
|--------|------|------|-----------------|-----------|
| `EMBEDDING_MODEL` | config.py | ~19 | `sentence-transformers/all-MiniLM-L6-v2` | Model chuyển text thành vector 384 chiều |
| `EMBEDDING_DIMENSION` | config.py | ~27 | `384` | Số chiều vector (khớp với model) |

**🎯 Cách chọn:**
- ✅ Nhanh & nhẹ: `all-MiniLM-L6-v2` (22MB, 384 chiều)
- 🔧 Chất lượng tốt: `all-mpnet-base-v2` (438MB, 768 chiều)
- 🇻🇳 Tiếng Việt: `paraphrase-multilingual-mpnet-base-v2`

---

### 2. CHROMA DATABASE (Lưu trữ Vector & Lịch sử)

| Tham số | Tệp | Dòng | Giá trị mặc định | Giải thích |
|--------|------|------|-----------------|-----------|
| `CHROMA_DB_PATH` | config.py | ~7 | `./chroma_db` | Đường dẫn lưu database |
| `CHROMA_COLLECTION_NAME` | config.py | ~10 | `ai_chatbox_documents` | Tên collection chứa tài liệu |
| `CHROMA_HISTORY_COLLECTION` | config.py | ~13 | `chat_history` | Tên collection chứa lịch sử |

---

### 3. LLM (Language Model - OpenAI)

| Tham số | Tệp | Dòng | Giá trị mặc định | Giải thích | Ảnh hưởng |
|--------|------|------|-----------------|-----------|----------|
| `OPENAI_API_KEY` | config.py | ~34 | `sk-your-api-key-here` | API key từ OpenAI | 🔐 Bắt buộc |
| `LLM_MODEL_NAME` | config.py | ~39 | `gpt-3.5-turbo` | Tên model LLM | 🧠 Chất lượng |
| `LLM_TEMPERATURE` | config.py | ~46 | `0.7` | Độ sáng tạo (0-1) | 🎲 Tính ngẫu nhiên |
| `LLM_MAX_TOKENS` | config.py | ~49 | `1024` | Độ dài tối đa phản hồi | 📝 Độ dài |

**LLM_MODEL_NAME - Các lựa chọn:**
```python
"gpt-3.5-turbo"        # ✅ Khuyến nghị - nhanh, rẻ
"gpt-4-turbo-preview"  # 🔧 Cao cấp - tốt hơn, chậm hơn
"gpt-4"                # 🏆 Tốt nhất - chậm, đắt nhất
```

**LLM_TEMPERATURE - Hướng dẫn:**
```python
0.0    # ❄️ Chính xác tuyệt đối
0.3    # ✅ Khuyến nghị - chính xác, ít sáng tạo
0.7    # ⚖️ Cân bằng
0.9    # 🔥 Sáng tạo, đa dạng
1.0    # 🎨 Ngẫu nhiên tối đa
```

**LLM_MAX_TOKENS - Giải thích:**
```python
256    # 🐜 Ngắn (1 đoạn)
512    # 📝 Vừa (vài đoạn)
1024   # ✅ Khuyến nghị (1-2 trang)
2048   # 📖 Dài (2-4 trang)
4096   # 📕 Rất dài (4+ trang)
```

---

### 4. RAG RETRIEVAL (Tìm kiếm tài liệu)

| Tham số | Tệp | Dòng | Giá trị mặc định | Giải thích | Ảnh hưởng |
|--------|------|------|-----------------|-----------|----------|
| `TOP_K_DOCUMENTS` | config.py | ~52 | `5` | Số tài liệu lấy ra | 🎯 Độ chính xác |
| `SIMILARITY_THRESHOLD` | config.py | ~55 | `0.5` | Ngưỡng độ tương tự | ✓ Tin cậy |
| `CHUNK_SIZE` | config.py | ~59 | `500` | Kích thước mỗi chunk | 📏 Chi tiết |
| `CHUNK_OVERLAP` | config.py | ~64 | `100` | Độ trùng lặp chunks | 🧠 Ngữ cảnh |

**TOP_K_DOCUMENTS - Cách chọn:**
```python
3      # ⚡ Nhanh, rẻ (chỉ top-3)
5      # ✅ Khuyến nghị (cân bằng)
10     # 🔍 Kỹ lưỡng (chi tiết hơn)
15+    # 📚 Tài liệu phức tạp (rất chi tiết)
```

**SIMILARITY_THRESHOLD - Hướng dẫn:**
```python
0.3    # 🤖 Linh hoạt (chấp nhận nhiều)
0.5    # ✅ Khuyến nghị (cân bằng)
0.7    # 📋 Nghiêm ngặt (chỉ tài liệu tương tự)
0.85   # 🔒 Cực kỳ nghiêm ngặt (an toàn)
```

**CHUNK_SIZE - Lựa chọn:**
```python
300    # ✂️ Nhỏ - chi tiết, ngữ cảnh ít
500    # ✅ Khuyến nghị - cân bằng tốt
800    # 📖 Lớn - ngữ cảnh dày đặc
1500   # 🏢 Rất lớn - tài liệu phức tạp
```

**CHUNK_OVERLAP - Công thức:**
```python
# Khuyến nghị: CHUNK_OVERLAP ≈ CHUNK_SIZE / 5

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100  # 500 / 5 = 100 ✅

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200  # 1000 / 5 = 200 ✅

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50   # 300 / 5 ≈ 50 ✅
```

---

### 5. PROMPT HỆ THỐNG (Hướng dẫn AI)

| Tham số | Tệp | Dòng | Giá trị mặc định | Giải thích |
|--------|------|------|-----------------|-----------|
| `SYSTEM_PROMPT` | config.py | ~82 | `Bạn là một trợ lý AI...` | Hướng dẫn AI cách ứng xử |

**💡 Ví dụ thay đổi:**

Mặc định:
```python
SYSTEM_PROMPT = """Bạn là một trợ lý AI thông minh và hữu ích.
Trả lời các câu hỏi dựa trên tài liệu được cung cấp.
Luôn trả lời bằng tiếng Việt."""
```

**Để AI chuyên môn Y tế:**
```python
SYSTEM_PROMPT = """Bạn là một chuyên gia Y tế. 
Trả lời các câu hỏi liên quan đến sức khỏe một cách chính xác.
Nếu câu hỏi nguy hiểm, hãy khuyến cáo nên tư vấn bác sĩ."""
```

**Để AI thân thiện:**
```python
SYSTEM_PROMPT = """Bạn là một người bạn thân thiện và tử tế.
Luôn tỏ ra quan tâm và sẵn sàng giúp đỡ.
Trả lời theo cách trò chuyện tự nhiên, không quá chính thức."""
```

---

### 6. FASTAPI SERVER

| Tham số | Tệp | Dòng | Giá trị mặc định | Giải thích |
|--------|------|------|-----------------|-----------|
| `API_HOST` | config.py | ~71 | `0.0.0.0` | IP server nghe |
| `API_PORT` | config.py | ~74 | `8000` | Cổng server |
| `API_RELOAD` | config.py | ~77 | `True` | Tự động reload code |

**API_HOST - Các lựa chọn:**
```python
"0.0.0.0"      # Tất cả IP có thể kết nối
"127.0.0.1"    # Chỉ localhost
"192.168.1.1"  # IP cụ thể nào đó
```

**API_PORT - Mẹo:**
```python
8000           # Mặc định, thường trống
8001, 8002     # Thay thế nếu 8000 bận
3000           # Port phổ biến khác
9000           # Port khác
```

**API_RELOAD:**
```python
True            # Dev mode - tự động reload
False           # Production - ổn định, tốc độ
```

---

### 7. LỊCH SỬ CHAT

| Tham số | Tệp | Dòng | Giá trị mặc định | Giải thích | Ảnh hưởng |
|--------|------|------|-----------------|-----------|----------|
| `MAX_HISTORY_MESSAGES` | config.py | ~87 | `20` | Số tin nhắn lưu | 💾 Bộ nhớ |

**Hướng dẫn:**
```python
5      # 🔋 Rất tiết kiệm
10     # 💨 Tiết kiệm
20     # ✅ Khuyến nghị (cân bằng)
50     # 📦 Bình thường
100+   # 💾 Lưu lâu, tốn RAM hơn
```

---

### 8. FILE TYPES

| Tham số | Tệp | Dòng | Giá trị mặc định | Giải thích |
|--------|------|------|-----------------|-----------|
| `ALLOWED_FILE_TYPES` | config.py | ~95 | `[".txt", ".pdf", ".md"]` | Loại file được phép |

**Ví dụ thêm file type:**
```python
ALLOWED_FILE_TYPES = [".txt", ".pdf", ".md", ".docx"]
```

---

## 🔧 CÁCH SỬA ĐỔI THAM SỐ

### Bước 1: Mở file config.py
```bash
# Windows
notepad config.py

# macOS/Linux
nano config.py
# hoặc
vim config.py
```

### Bước 2: Tìm tham số

Ví dụ: Muốn tăng `TOP_K_DOCUMENTS` từ 5 → 10

Tìm dòng:
```python
TOP_K_DOCUMENTS = 5
```

### Bước 3: Chỉnh sửa

Đổi thành:
```python
TOP_K_DOCUMENTS = 10
```

### Bước 4: Lưu file

- **VS Code**: Ctrl+S
- **Notepad**: Ctrl+S
- **Vim**: Esc → :wq → Enter

### Bước 5: Khởi động lại server

```bash
# Dừng server hiện tại: Ctrl+C
# Khởi động lại
python main.py
```

---

## 📈 BẢNG SO SÁNH - THAM SỐ NHANH

### Scenario 1: Muốn AI Thông Minh (Chất lượng cao)

```python
# config.py
LLM_MODEL_NAME = "gpt-4"                    # Model tốt nhất
LLM_TEMPERATURE = 0.3                       # Chính xác
TOP_K_DOCUMENTS = 15                        # Tìm kỹ
SIMILARITY_THRESHOLD = 0.3                  # Linh hoạt
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"  # Model tốt
CHUNK_SIZE = 800                            # Ngữ cảnh nhiều
```

**Kết quả**: 🧠 AI thông minh nhất | ⏱️ Chậm | 💰 Đắt nhất

---

### Scenario 2: Muốn Nhanh & Rẻ (Chi phí thấp)

```python
# config.py
LLM_MODEL_NAME = "gpt-3.5-turbo"            # Model rẻ
LLM_TEMPERATURE = 0.9                       # Phản hồi nhanh
TOP_K_DOCUMENTS = 3                         # Ít tài liệu
SIMILARITY_THRESHOLD = 0.7                  # Nghiêm ngặt
LLM_MAX_TOKENS = 256                        # Phản hồi ngắn
CHUNK_SIZE = 300                            # Chunks nhỏ
```

**Kết quả**: ⚡ Nhanh nhất | 💰 Rẻ nhất | 🧠 Chất lượng khá

---

### Scenario 3: Cân bằng (Khuyến nghị)

```python
# config.py
LLM_MODEL_NAME = "gpt-3.5-turbo"            # Cân bằng
LLM_TEMPERATURE = 0.7                       # Cân bằng
TOP_K_DOCUMENTS = 5                         # Cân bằng
SIMILARITY_THRESHOLD = 0.5                  # Cân bằng
LLM_MAX_TOKENS = 1024                       # Vừa phải
CHUNK_SIZE = 500                            # Vừa phải
```

**Kết quả**: ⚖️ Cân bằng tốt | ✅ Khuyến nghị

---

### Scenario 4: Chuyên môn (Y tế, Pháp lý)

```python
# config.py
LLM_MODEL_NAME = "gpt-4"                    # Tốt nhất
LLM_TEMPERATURE = 0.2                       # Cực chính xác
TOP_K_DOCUMENTS = 20                        # Rất kỹ
SIMILARITY_THRESHOLD = 0.85                 # Rất nghiêm ngặt
SYSTEM_PROMPT = """Bạn là chuyên gia [lĩnh vực]."""
```

**Kết quả**: 📋 Cực kỳ chính xác | 🔒 An toàn

---

## ❓ CÂU HỎI THƯỜNG GẶP

**Q: Thay đổi tham số có cần khởi động lại server không?**
A: ✅ CÓ. Khởi động lại: `python main.py`

**Q: Thay đổi cái nào ảnh hưởng nhất?**
A: `LLM_MODEL_NAME` → `TOP_K_DOCUMENTS` → `LLM_TEMPERATURE`

**Q: Để tiết kiệm OpenAI API cost?**
A: Giảm `LLM_MAX_TOKENS` & `TOP_K_DOCUMENTS`

**Q: Để AI trả lời chính xác hơn?**
A: Giảm `LLM_TEMPERATURE` & tăng `TOP_K_DOCUMENTS`

**Q: Để server chạy nhanh hơn?**
A: Giảm `CHUNK_SIZE` & `TOP_K_DOCUMENTS`

---

**✅ Hãy thử các tham số khác nhau để tìm setup tốt nhất cho nhu cầu của bạn!**

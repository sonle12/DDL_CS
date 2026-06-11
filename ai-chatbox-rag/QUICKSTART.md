# 🚀 QUICK START - HƯỚNG DẪN NHANH

> **Thực hiện từng bước dưới đây để chạy hệ thống trong 5 phút**

---

## ⏱️ BƯỚC 1: CÀI ĐẶT PYTHON (5 phút)

### 1a. Kiểm tra Python đã cài chưa

```bash
python --version
# Kết quả: Python 3.8+ ✅
```

### 1b. Nếu chưa cài, tải từ: https://www.python.org/

---

## ⏱️ BƯỚC 2: CÀI ĐẶT THƯ VIỆN (3-5 phút)

```bash
# Vào thư mục dự án
cd ai-chatbox-rag

# Cài các thư viện (tự động download ~500MB)
pip install -r requirements.txt
```

⏳ **Chờ đợi**... (có thể mất 3-5 phút)

✅ **Hoàn thành khi thấy**: `Successfully installed ...`

---

## ⏱️ BƯỚC 3: LẤY OPENAI API KEY (2 phút)

### 3a. Truy cập: https://platform.openai.com/account/api-keys

### 3b. Click "+ Create new secret key"

### 3c. Copy key được tạo (bắt đầu bằng `sk-`)

### 3d. Đặt environment variable

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY = "sk-..."  # Dán key của bạn ở đây
```

**Windows CMD:**
```cmd
set OPENAI_API_KEY=sk-...
```

**macOS/Linux:**
```bash
export OPENAI_API_KEY="sk-..."
```

✅ **Kiểm tra**: 
```bash
echo $env:OPENAI_API_KEY  # Windows PowerShell
echo $OPENAI_API_KEY      # macOS/Linux
```

---

## ⏱️ BƯỚC 4: CHẠY DEMO (2 phút)

```bash
# Test hệ thống có hoạt động không
python demo.py
```

**Kết quả mong muốn:**
```
🚀 DEMO HỆ THỐNG RAG
🎉 DEMO HOÀN THÀNH!
```

---

## ⏱️ BƯỚC 5: CHẠY SERVER (30 giây)

```bash
python main.py
```

**Kết quả:**
```
🎉 KHỞI ĐỘNG SERVER
🌐 Server sẽ chạy tại: http://0.0.0.0:8000
📚 API Documentation: http://localhost:8000/docs
```

✅ **Server chạy bình thường!**

---

## 🧪 BƯỚC 6: TEST API (Cửa sổ terminal mới)

### Cách 1: Dùng Web Interface (Dễ nhất)

1. Mở browser
2. Truy cập: **http://localhost:8000/docs**
3. Sẽ thấy giao diện Swagger - Click vào các endpoint để test

### Cách 2: Dùng curl command

#### 2a. Thêm tài liệu mẫu

```bash
curl -X POST http://localhost:8000/add-documents \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      "Công ty ABC có 500 nhân viên, chuyên phát triển phần mềm."
    ],
    "metadata": [{"source": "company.txt"}]
  }'
```

#### 2b. Chat

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Công ty ABC có bao nhiêu nhân viên?",
    "user_id": "user_1"
  }'
```

**Kết quả:**
```json
{
  "answer": "Công ty ABC có 500 nhân viên",
  "question": "Công ty ABC có bao nhiêu nhân viên?",
  "relevant_documents": [...]
}
```

✅ **Thành công!**

---

## 📝 CÁC BƯỚC TIẾP THEO

### ✅ Sau khi demo thành công:

1. **Thêm tài liệu của bạn**
   - Upload file `.txt` hoặc `.md`
   - Hoặc gửi text trực tiếp qua API

2. **Tối ưu tham số**
   - Mở `PARAMETERS.md` để xem hướng dẫn tối ưu

3. **Cấu hình API key**
   - Tạo file `.env` từ `.env.example` (an toàn hơn)

4. **Deploy lên server**
   - Chạy trên VPS/Cloud (AWS, Google Cloud, ...)
   - Dùng Docker để deploy dễ hơn

---

## 🆘 LỖI THƯỜNG GẶP

### ❌ `pip: command not found`
**Giải pháp**: Python chưa cài đặt hoặc PATH sai
- Cài Python từ https://www.python.org/
- Chọn "Add Python to PATH" khi cài

### ❌ `ModuleNotFoundError: No module named 'openai'`
**Giải pháp**: Thư viện chưa cài
```bash
pip install -r requirements.txt
```

### ❌ `OPENAI_API_KEY not found`
**Giải pháp**: Kiểm tra API key
```bash
echo $OPENAI_API_KEY  # Phải in ra key
```

### ❌ `Port 8000 already in use`
**Giải pháp**: Thay đổi port trong `config.py`
```python
API_PORT = 8001  # hoặc số khác
```

### ❌ `Connection refused localhost:8000`
**Giải pháp**: Server chưa chạy
```bash
python main.py  # Hãy chạy server trước
```

---

## 📚 TÀI LIỆU HƯỚNG DẪN

- **Chi tiết**: `README.md`
- **Tham số**: `PARAMETERS.md`
- **API**: http://localhost:8000/docs (khi server chạy)

---

## ✨ XIN CHÚC MỪNG!

🎉 Bạn đã thiết lập thành công hệ thống AI Chatbox RAG!

**Tiếp theo:**
1. Thêm tài liệu của bạn
2. Chat với AI
3. Tối ưu tham số cho nhu cầu của bạn
4. Triển khai lên production

**Vui lòng liên hệ nếu có vấn đề!**

# ============================================================================
# TÀI LIỆU CẤU HÌNH - THAM SỐ QUAN TRỌNG
# ============================================================================
# Đây là file chứa tất cả tham số quan trọng. 
# Thay đổi các giá trị dưới đây để điều chỉnh hành vi của AI
# ============================================================================

import os
from typing import Optional

# ============================================================================
# 1. CẤU HÌNH CHROMA DB (Lưu trữ Vector & Lịch sử)
# ============================================================================
CHROMA_DB_PATH = "./chroma_db"  
# 📌 THAM SỐ: Đường dẫn lưu trữ database ChromaDB (lưu vector embedding)
# THAY ĐỔI KHI: Muốn đặt database ở vị trí khác

CHROMA_COLLECTION_NAME = "ai_chatbox_documents"
# 📌 THAM SỐ: Tên collection trong ChromaDB (coi như tên bảng)
# THAY ĐỔI KHI: Muốn quản lý nhiều collection riêng biệt

CHROMA_HISTORY_COLLECTION = "chat_history"
# 📌 THAM SỐ: Collection riêng để lưu lịch sử chat
# THAY ĐỔI KHI: Muốn lưu lịch sử ở collection khác

# ============================================================================
# 2. CẤU HÌNH EMBEDDING MODEL (Model chuyển văn bản thành vector)
# ============================================================================
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# 📌 THAM SỐ: Model embedding. Các lựa chọn:
#   - "sentence-transformers/all-MiniLM-L6-v2" (nhẹ, nhanh, ~22MB) ✅ KHUYẾN NGHỊ
#   - "sentence-transformers/all-mpnet-base-v2" (tốt hơn, chậm hơn, ~438MB)
#   - "sentence-transformers/paraphrase-multilingual-mpnet-base-v2" (hỗ trợ đa ngôn ngữ)
#   - "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2" (nhẹ, đa ngôn ngữ)
# THAY ĐỔI KHI: Muốn tăng chất lượng embedding (model lớn hơn) hoặc hỗ trợ tiếng Việt tốt hơn
# LƯU Ý: Model lớn = chất lượng tốt hơn nhưng tốn RAM & chậm hơn

EMBEDDING_DIMENSION = 384
# 📌 THAM SỐ: Số chiều của vector embedding
# THAY ĐỔI KHI: Thay đổi EMBEDDING_MODEL (phải khớp với model)
# LƯU Ý: all-MiniLM-L6-v2 = 384 chiều, all-mpnet-base-v2 = 768 chiều

# ============================================================================
# 3. CẤU HÌNH LLM (Large Language Model - OpenAI hoặc model khác)
# ============================================================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-your-api-key-here")
# 📌 THAM SỐ: API key từ OpenAI
# THAY ĐỔI KHI: Cần chuyển sang OpenAI key khác
# LƯU Ý: Đặt environment variable OPENAI_API_KEY thay vì code cứng

LLM_MODEL_NAME = "gpt-3.5-turbo"
# 📌 THAM SỐ: Tên model LLM. Các lựa chọn:
#   - "gpt-3.5-turbo" (nhanh, rẻ, khá tốt) ✅ KHUYẾN NGHỊ
#   - "gpt-4" (rất thông minh, chậm, đắt)
#   - "gpt-4-turbo-preview" (balance giữa chất lượng & tốc độ)
# THAY ĐỔI KHI: Muốn AI thông minh hơn (dùng gpt-4) hoặc rẻ hơn

LLM_TEMPERATURE = 0.7
# 📌 THAM SỐ: Mức sáng tạo của AI (0 = chính xác, 1 = sáng tạo)
# THAY ĐỔI KHI: 
#   - Muốn AI chính xác hơn: đổi thành 0.3 (ít ngẫu nhiên)
#   - Muốn AI sáng tạo hơn: đổi thành 0.9 (phản hồi đa dạng)

LLM_MAX_TOKENS = 1024
# 📌 THAM SỐ: Độ dài tối đa của phản hồi (số từ)
# THAY ĐỔI KHI: 
#   - Muốn phản hồi dài hơn: tăng lên 2048
#   - Muốn phản hồi ngắn hơn: giảm xuống 512

# ============================================================================
# 4. CẤU HÌNH RAG (Retrieval-Augmented Generation - Tìm kiếm tài liệu)
# ============================================================================
TOP_K_DOCUMENTS = 5
# 📌 THAM SỐ: Số lượng tài liệu tương tự nhất được truy xuất
# THAY ĐỔI KHI:
#   - Muốn AI chính xác hơn: tăng lên 7-10 (tìm kiếm kỹ hơn)
#   - Muốn nhanh hơn & tiết kiệm chi phí: giảm xuống 3
# LƯU Ý: Tăng TOP_K = AI tốt hơn nhưng chậm hơn

SIMILARITY_THRESHOLD = 0.5
# 📌 THAM SỐ: Ngưỡng độ tương tự (0-1). Chỉ lấy tài liệu có độ tương tự >= ngưỡng
# THAY ĐỔI KHI:
#   - Muốn AI chỉ trả lời khi chắc chắn: tăng lên 0.7-0.8
#   - Muốn AI linh hoạt hơn: giảm xuống 0.3
# LƯU Ý: Cao = nghiêm ngặt, Thấp = thỏa thuận

CHUNK_SIZE = 500
# 📌 THAM SỐ: Kích thước mỗi đoạn văn bản khi chia tài liệu
# THAY ĐỔI KHI:
#   - Tài liệu phức tạp: tăng lên 800-1000
#   - Tài liệu đơn giản: giảm xuống 300
# LƯU Ý: Nhỏ = chi tiết hơn, Lớn = ngữ cảnh nhiều hơn

CHUNK_OVERLAP = 100
# 📌 THAM SỐ: Độ trùng lặp giữa các chunk (để giữ ngữ cảnh)
# THAY ĐỔI KHI: Muốn thêm/bớt ngữ cảnh liên kết
# LƯU Ý: Thường = CHUNK_SIZE / 4 hoặc 1/5

# ============================================================================
# 5. CẤU HÌNH FASTAPI SERVER
# ============================================================================
API_HOST = "0.0.0.0"
# 📌 THAM SỐ: IP nghe (0.0.0.0 = tất cả IP)
# THAY ĐỔI KHI: Chỉ muốn localhost truy cập → "127.0.0.1"

API_PORT = 8000
# 📌 THAM SỐ: Cổng chạy API
# THAY ĐỔI KHI: Port 8000 bị chiếm → thay số khác (8001, 9000, ...)

API_RELOAD = True
# 📌 THAM SỐ: Tự động reload khi code thay đổi (dev mode)
# THAY ĐỔI KHI: Chạy production → đổi thành False

# ============================================================================
# 6. CẤU HÌNH PROMPT HỆ THỐNG (System prompt)
# ============================================================================
SYSTEM_PROMPT = """Bạn là một trợ lý AI thông minh và hữu ích.
Trả lời các câu hỏi dựa trên tài liệu được cung cấp.
Luôn trả lời bằng tiếng Việt.
Nếu không tìm thấy thông tin trong tài liệu, hãy nói rõ ràng.
Hãy cộng tác và lịch sự trong mọi tương tác."""
# 📌 THAM SỐ: Hướng dẫn AI cách ứng xử
# THAY ĐỔI KHI: Muốn AI có tính cách khác
# VÍ DỤ: Đổi thành "Bạn là một chuyên gia về Y tế..." để AI chuyên môn hơn

# ============================================================================
# 7. CẤU HÌNH LƯU LỊCH SỬ CHAT
# ============================================================================
MAX_HISTORY_MESSAGES = 20
# 📌 THAM SỐ: Số tin nhắn lịch sử tối đa được lưu
# THAY ĐỔI KHI:
#   - Muốn AI nhớ lâu hơn: tăng lên 50-100
#   - Muốn tiết kiệm tài nguyên: giảm xuống 5-10

# ============================================================================
# 8. CẤU HÌNH XỬ LÝ TÀI LIỆU
# ============================================================================
ALLOWED_FILE_TYPES = [".txt", ".pdf", ".md"]
# 📌 THAM SỐ: Các loại file được phép upload
# THAY ĐỔI KHI: Muốn support thêm file type khác

# ============================================================================
# TÓMLƯỢC CẤU HÌNH NHANH CHÓNG
# ============================================================================
"""
🚀 Để AI THÔNG MINH HƠN:
   1. Tăng TOP_K_DOCUMENTS từ 5 → 10
   2. Đổi LLM_MODEL_NAME từ gpt-3.5-turbo → gpt-4
   3. Giảm SIMILARITY_THRESHOLD từ 0.5 → 0.3

📊 Để NHANH HƠN & RẺ HƠN:
   1. Giảm TOP_K_DOCUMENTS từ 5 → 3
   2. Tăng LLM_TEMPERATURE từ 0.7 → 0.9 (phản hồi nhanh)
   3. Giảm LLM_MAX_TOKENS từ 1024 → 512

🎯 Để AI NHỚ CÁC CUỘC HỘI THOẠI ĐẦY ĐỦ:
   1. Tăng MAX_HISTORY_MESSAGES từ 20 → 100
   
💾 Để AI CHÍNH XÁC HƠN:
   1. Giảm LLM_TEMPERATURE từ 0.7 → 0.3
   2. Tăng SIMILARITY_THRESHOLD từ 0.5 → 0.8
"""

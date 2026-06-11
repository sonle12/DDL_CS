# ============================================================================
# FASTAPI SERVER CHO AI CHATBOX
# ============================================================================
# API server để interact với RAG system qua HTTP requests
# Endpoints: 
#   - POST /chat: Gửi câu hỏi và nhận phản hồi
#   - POST /add-documents: Thêm tài liệu vào hệ thống
#   - GET /history: Lấy lịch sử chat
#   - GET /stats: Lấy thống kê hệ thống
#   - DELETE /clear: Xóa tất cả tài liệu
# ============================================================================

import os
import sys
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import hệ thống RAG
from rag_system import RAGSystem, load_text_file, load_multiple_files
from config import (
    API_HOST, API_PORT, API_RELOAD, SYSTEM_PROMPT, MAX_HISTORY_MESSAGES
)


# ============================================================================
# ĐỊNH NGHĨA CẤU TRÚC DỮ LIỆU (Pydantic Models)
# ============================================================================

class ChatRequest(BaseModel):
    """
    📝 CẤU TRÚC YÊU CẦU CHAT
    
    Ví dụ:
    {
        "question": "Công ty X có bao nhiêu nhân viên?",
        "user_id": "user_123"  (tùy chọn)
    }
    """
    question: str  # 📌 THAM SỐ: Câu hỏi từ user
    user_id: str = "default"  # 📌 THAM SỐ: ID người dùng (để lưu lịch sử riêng)


class ChatResponse(BaseModel):
    """
    📤 CẤU TRÚC PHẢN HỒI CHAT
    
    Trả về:
    - question: Câu hỏi gốc
    - answer: Câu trả lời từ AI
    - relevant_documents: Tài liệu được sử dụng
    - timestamp: Thời gian xử lý
    """
    question: str
    answer: str
    relevant_documents: List[Dict]
    timestamp: str


class DocumentRequest(BaseModel):
    """
    📑 CẤU TRÚC THÊM TÀI LIỆU
    
    Ví dụ:
    {
        "documents": ["Nội dung tài liệu 1", "Nội dung tài liệu 2"],
        "metadata": [{"source": "file1.txt"}, {"source": "file2.txt"}]
    }
    """
    documents: List[str]  # 📌 THAM SỐ: Danh sách tài liệu
    metadata: Optional[List[Dict]] = None  # 📌 THAM SỐ: Thông tin về tài liệu


class HistoryResponse(BaseModel):
    """
    📜 CẤU TRÚC LỊCH SỬ CHAT
    """
    user_id: str
    history: List[Dict]


# ============================================================================
# KHỞI TẠO FASTAPI ỨNG DỤNG
# ============================================================================

app = FastAPI(
    title="🤖 AI Chatbox RAG",
    description="Hệ thống AI chatbox sử dụng RAG (Retrieval-Augmented Generation)",
    version="1.0.0"
)

# ✅ Thêm CORS middleware (cho phép requests từ frontend)
# 📌 THAM SỐ: allow_origins - danh sách domain được phép
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 📌 "*" = cho phép tất cả (dev), dùng danh sách cụ thể cho prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Khởi tạo RAG System (tạo vector store, LLM, ...)
# 📌 Điều này xảy ra khi server khởi động
print("=" * 70)
print("🚀 KHỞI ĐỘNG SERVER AI CHATBOX...")
print("=" * 70)

try:
    rag_system = RAGSystem()
    system_ready = True
except Exception as e:
    print(f"❌ LỖI KHỞI TẠO HỆ THỐNG: {e}")
    system_ready = False


# ============================================================================
# ENDPOINT 1: ROOT (TEST KẾT NỐI)
# ============================================================================

@app.get("/")
async def root():
    """
    🏠 ENDPOINT TEST
    
    Dùng để kiểm tra xem server có hoạt động không
    
    Ví dụ curl:
    curl http://localhost:8000/
    """
    return {
        "message": "✅ AI Chatbox RAG Server đang chạy!",
        "status": "ready" if system_ready else "error",
        "api_version": "1.0.0"
    }


# ============================================================================
# ENDPOINT 2: HEALTH CHECK
# ============================================================================

@app.get("/health")
async def health():
    """
    💚 KIỂM TRA TRẠNG THÁI HỆ THỐNG
    
    Trả về thông tin về trạng thái server và RAG system
    
    Ví dụ curl:
    curl http://localhost:8000/health
    """
    if not system_ready:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    stats = rag_system.get_stats()
    return {
        "status": "healthy",
        "system_stats": stats,
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# ENDPOINT 3: CHAT (CHÍNH)
# ============================================================================

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    💬 ENDPOINT CHAT CHÍNH
    
    Nhận câu hỏi và trả về phản hồi dựa trên tài liệu trong RAG system
    
    Quy trình:
    1. Nhận câu hỏi từ client
    2. Gửi tới RAG system
    3. RAG system tìm kiếm tài liệu + gọi LLM
    4. Trả về phản hồi + tài liệu tham khảo
    
    Ví dụ curl:
    curl -X POST http://localhost:8000/chat \\
      -H "Content-Type: application/json" \\
      -d '{
        "question": "Công ty X có bao nhiêu nhân viên?",
        "user_id": "user_123"
      }'
    
    💡 THAY ĐỔI ĐỂ AI TỐT HƠN:
    - Tăng TOP_K_DOCUMENTS (config.py): Tìm kiếm kỹ hơn
    - Giảm SIMILARITY_THRESHOLD: Linh hoạt hơn
    - Thay đổi LLM_TEMPERATURE: Điều chỉnh độ sáng tạo
    """
    try:
        if not system_ready:
            raise HTTPException(status_code=503, detail="RAG System not initialized")
        
        # ✅ Gọi RAG system để xử lý câu hỏi
        result = rag_system.query(
            question=request.question,
            user_id=request.user_id
        )
        
        return ChatResponse(
            question=result["question"],
            answer=result["answer"],
            relevant_documents=result["relevant_documents"],
            timestamp=result["timestamp"]
        )
    
    except Exception as e:
        print(f"❌ Lỗi trong endpoint /chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINT 4: THÊM TÀI LIỆU (VẬN BẢN BẢN)
# ============================================================================

@app.post("/add-documents")
async def add_documents(request: DocumentRequest):
    """
    📥 ENDPOINT THÊM TÀI LIỆU (TEXT TRỰC TIẾP)
    
    Thêm tài liệu text trực tiếp vào hệ thống
    
    Ví dụ curl:
    curl -X POST http://localhost:8000/add-documents \\
      -H "Content-Type: application/json" \\
      -d '{
        "documents": [
          "Công ty X được thành lập năm 2020. X có 500 nhân viên.",
          "Công ty X chuyên lĩnh vực công nghệ. Trụ sở chính ở Hà Nội."
        ],
        "metadata": [
          {"source": "company_info.txt"},
          {"source": "company_profile.txt"}
        ]
      }'
    
    💡 THAY ĐỔI ĐỂ AI TỐT HƠN:
    - Thêm nhiều tài liệu: AI sẽ thông minh hơn
    - Chọn tài liệu chất lượng: Tránh thông tin sai lệch
    - Chuẩn bị dữ liệu sạch: Loại bỏ ký tự lạ, định dạng đúng
    """
    try:
        if not system_ready:
            raise HTTPException(status_code=503, detail="RAG System not initialized")
        
        # ✅ Gọi RAG system để thêm tài liệu
        rag_system.add_documents(
            documents=request.documents,
            metadata_list=request.metadata
        )
        
        return {
            "status": "success",
            "message": f"✅ Thêm {len(request.documents)} tài liệu thành công",
            "num_documents": len(request.documents),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        print(f"❌ Lỗi trong endpoint /add-documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINT 5: THÊM TÀI LIỆU (UPLOAD FILE)
# ============================================================================

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    """
    📤 ENDPOINT UPLOAD FILE
    
    Upload file text (.txt, .md) và thêm vào hệ thống
    
    Ví dụ curl:
    curl -X POST http://localhost:8000/upload-file \\
      -F "file=@path/to/your/file.txt"
    
    💡 HỖ TRỢ CÁC FORMAT:
    - .txt: Text file
    - .md: Markdown file (được xử lý như text)
    """
    try:
        if not system_ready:
            raise HTTPException(status_code=503, detail="RAG System not initialized")
        
        # ✅ Đọc nội dung file
        content = await file.read()
        content_str = content.decode("utf-8")
        
        # ✅ Thêm vào hệ thống
        rag_system.add_documents(
            documents=[content_str],
            metadata_list=[{"source": file.filename}]
        )
        
        return {
            "status": "success",
            "message": f"✅ Upload file '{file.filename}' thành công",
            "filename": file.filename,
            "size": len(content_str),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        print(f"❌ Lỗi trong endpoint /upload-file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINT 6: LẤY LỊCH SỬ CHAT
# ============================================================================

@app.get("/history/{user_id}", response_model=HistoryResponse)
async def get_history(user_id: str, limit: int = MAX_HISTORY_MESSAGES):
    """
    📜 ENDPOINT LẤY LỊCH SỬ CHAT
    
    Lấy lịch sử chat của một user
    
    Tham số:
    - user_id: ID người dùng (trong URL)
    - limit: Số tin nhắn tối đa (query param, mặc định = 20)
    
    Ví dụ curl:
    curl http://localhost:8000/history/user_123
    curl http://localhost:8000/history/user_123?limit=50
    
    💡 THAM SỐ CẦN THAY ĐỔI:
    - limit: MAX_HISTORY_MESSAGES (config.py)
      * Tăng để nhớ lâu hơn
      * Giảm để tiết kiệm tài nguyên
    """
    try:
        if not system_ready:
            raise HTTPException(status_code=503, detail="RAG System not initialized")
        
        # ✅ Lấy lịch sử từ RAG system
        history = rag_system.get_history(
            user_id=user_id,
            limit=limit
        )
        
        return HistoryResponse(
            user_id=user_id,
            history=history
        )
    
    except Exception as e:
        print(f"❌ Lỗi trong endpoint /history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINT 7: LẤY THỐNG KÊ HỆ THỐNG
# ============================================================================

@app.get("/stats")
async def get_stats():
    """
    📊 ENDPOINT LẤY THỐNG KÊ
    
    Lấy thông tin thống kê về hệ thống
    
    Trả về:
    - Số tài liệu trong hệ thống
    - Model embedding
    - Model LLM
    - Các tham số cấu hình
    
    Ví dụ curl:
    curl http://localhost:8000/stats
    """
    try:
        if not system_ready:
            raise HTTPException(status_code=503, detail="RAG System not initialized")
        
        stats = rag_system.get_stats()
        return {
            "status": "success",
            "stats": stats,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        print(f"❌ Lỗi trong endpoint /stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINT 8: XÓA TẤT CẢ TÀI LIỆU
# ============================================================================

@app.delete("/clear")
async def clear_all():
    """
    🗑️  ENDPOINT XÓA TÀI LIỆU
    
    ⚠️  CẢNH BÁO: Xóa tất cả tài liệu! Không thể khôi phục!
    
    Ví dụ curl:
    curl -X DELETE http://localhost:8000/clear
    """
    try:
        if not system_ready:
            raise HTTPException(status_code=503, detail="RAG System not initialized")
        
        rag_system.clear_documents()
        
        return {
            "status": "success",
            "message": "✅ Xóa tất cả tài liệu thành công",
            "warning": "⚠️  Dữ liệu đã bị xóa vĩnh viễn!",
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        print(f"❌ Lỗi trong endpoint /clear: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINT 9: TẢI TÀI LIỆU TỪ FOLDER
# ============================================================================

@app.post("/load-folder")
async def load_folder(
    folder_path: str = Form(...),
    file_pattern: str = Form(default="*.txt")
):
    """
    📁 ENDPOINT TẢI TÀI LIỆU TỪ THƯ MỤC
    
    Tải tất cả file từ một thư mục
    
    Tham số:
    - folder_path: Đường dẫn thư mục
    - file_pattern: Pattern file (*.txt, *.md, ...)
    
    Ví dụ curl:
    curl -X POST http://localhost:8000/load-folder \\
      -d "folder_path=/path/to/documents" \\
      -d "file_pattern=*.txt"
    
    💡 LỢI ÍCH:
    - Tải hàng loạt file
    - Tự động xử lý tất cả
    - Nhanh chóng chuẩn bị dữ liệu
    """
    try:
        if not system_ready:
            raise HTTPException(status_code=503, detail="RAG System not initialized")
        
        # ✅ Kiểm tra folder tồn tại
        if not os.path.isdir(folder_path):
            raise HTTPException(status_code=400, detail=f"Folder không tồn tại: {folder_path}")
        
        # ✅ Tải tài liệu từ folder
        documents = load_multiple_files(folder_path, file_pattern)
        
        if not documents:
            raise HTTPException(status_code=400, detail=f"Không tìm thấy file với pattern: {file_pattern}")
        
        # ✅ Thêm vào hệ thống
        metadata_list = [{"source": f"folder_import_{i}"} for i in range(len(documents))]
        rag_system.add_documents(documents=documents, metadata_list=metadata_list)
        
        return {
            "status": "success",
            "message": f"✅ Tải {len(documents)} file từ folder thành công",
            "num_documents": len(documents),
            "folder": folder_path,
            "pattern": file_pattern,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        print(f"❌ Lỗi trong endpoint /load-folder: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CHẠY SERVER
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🎉 KHỞI ĐỘNG SERVER")
    print("=" * 70)
    print(f"🌐 Server sẽ chạy tại: http://{API_HOST}:{API_PORT}")
    print(f"📚 API Documentation: http://localhost:{API_PORT}/docs")
    print(f"🔄 OpenAPI Schema: http://localhost:{API_PORT}/openapi.json")
    print("=" * 70)
    print("Nhấn Ctrl+C để dừng server\n")
    
    # Khởi động Uvicorn server
    # 📌 THAM SỐ:
    #   - host: IP nghe (0.0.0.0 = tất cả IP)
    #   - port: Cổng (8000, 8001, ...)
    #   - reload: Tự động reload khi code thay đổi (dev mode)
    #   - log_level: Mức log (debug, info, warning, error)
    uvicorn.run(
        "main:app",
        host=API_HOST,  # 📌 Thay đổi để chỉ định IP
        port=API_PORT,  # 📌 Thay đổi cổng nếu cần
        reload=API_RELOAD,  # 📌 Tắt khi chạy production
        log_level="info"  # 📌 Thay đổi thành "debug" để xem chi tiết
    )

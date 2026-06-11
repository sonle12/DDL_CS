# ============================================================================
# FILE KHỞI ĐỘNG NHANH - DEMO
# ============================================================================
# Chạy script này để tự động test hệ thống RAG
# 
# Lưu ý: 
# - Cần cài đặt requirements.txt trước
# - Cần thiết lập OPENAI_API_KEY
# ============================================================================

import sys
from rag_system import RAGSystem, load_text_file
from config import TOP_K_DOCUMENTS, SIMILARITY_THRESHOLD

def main():
    print("=" * 70)
    print("🚀 DEMO HỆ THỐNG RAG")
    print("=" * 70)
    
    # ✅ BƯỚC 1: Khởi tạo RAG System
    print("\n📚 [BƯỚC 1] Khởi tạo hệ thống RAG...")
    try:
        rag = RAGSystem()
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return
    
    # ✅ BƯỚC 2: Thêm tài liệu mẫu
    print("\n📥 [BƯỚC 2] Thêm tài liệu mẫu...")
    
    sample_documents = [
        """
        Công ty ABC được thành lập năm 2020 bởi các kỹ sư công nghệ.
        Công ty ABC chuyên phát triển phần mềm quản lý doanh nghiệp (ERP).
        Hiện tại, công ty ABC có 150 nhân viên tại Hà Nội và Hồ Chí Minh.
        """,
        """
        Sản phẩm chính của ABC là nền tảng cloud-based ERP.
        Nền tảng này giúp các doanh nghiệp quản lý tài chính, kho hàng, nhân sự.
        Đã có hơn 500 doanh nghiệp sử dụng sản phẩm của ABC.
        """,
        """
        Công ty ABC đã nhận được tài trợ Series A từ các nhà đầu tư hàng đầu.
        Vòng tài trợ này giúp ABC mở rộng thị trường sang Đông Nam Á.
        Kế hoạch trong 2 năm tới: Nhân lên 500 nhân viên.
        """
    ]
    
    metadata = [
        {"source": "company_overview.txt", "type": "general"},
        {"source": "products.txt", "type": "product"},
        {"source": "news.txt", "type": "news"}
    ]
    
    try:
        rag.add_documents(sample_documents, metadata)
        print("✅ Thêm tài liệu mẫu thành công")
    except Exception as e:
        print(f"❌ Lỗi khi thêm tài liệu: {e}")
        return
    
    # ✅ BƯỚC 3: Thống kê
    print("\n📊 [BƯỚC 3] Thống kê hệ thống...")
    stats = rag.get_stats()
    print(f"📈 Số tài liệu: {stats.get('total_documents', 0)}")
    print(f"🔍 Embedding model: {stats.get('embedding_model', 'N/A')}")
    print(f"🤖 LLM model: {stats.get('llm_model', 'N/A')}")
    print(f"📌 Top-K: {stats.get('top_k', 0)}")
    print(f"📏 Similarity threshold: {stats.get('similarity_threshold', 0)}")
    
    # ✅ BƯỚC 4: Chat
    print("\n💬 [BƯỚC 4] Demo chat...")
    questions = [
        "Công ty ABC có bao nhiêu nhân viên?",
        "Sản phẩm chính của ABC là gì?",
        "ABC đã nhận tài trợ bao nhiêu?"
    ]
    
    for question in questions:
        print(f"\n❓ Câu hỏi: {question}")
        result = rag.query(question, user_id="demo_user")
        print(f"✅ Trả lời: {result['answer'][:200]}...")  # In 200 ký tự đầu
        print(f"📚 Số tài liệu liên quan: {len(result['relevant_documents'])}")
        if result['relevant_documents']:
            print(f"   - Độ tương tự cao nhất: {result['relevant_documents'][0]['similarity']:.2%}")
    
    # ✅ BƯỚC 5: Lịch sử
    print("\n📜 [BƯỚC 5] Lấy lịch sử chat...")
    history = rag.get_history("demo_user", limit=5)
    print(f"📋 Số tin nhắn trong lịch sử: {len(history)}")
    for i, item in enumerate(history[:3], 1):
        print(f"   {i}. Q: {item['question'][:50]}...")
    
    print("\n" + "=" * 70)
    print("🎉 DEMO HOÀN THÀNH!")
    print("=" * 70)
    print("\n✅ Hệ thống RAG hoạt động bình thường")
    print("🚀 Bây giờ bạn có thể chạy: python main.py")
    print("📚 Truy cập API tại: http://localhost:8000/docs")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo dừng lại")
    except Exception as e:
        print(f"\n❌ Lỗi không mong muốn: {e}")
        import traceback
        traceback.print_exc()

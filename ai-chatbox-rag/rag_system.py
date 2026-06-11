# ============================================================================
# HỆ THỐNG RAG (RETRIEVAL-AUGMENTED GENERATION) CHÍ TIẾT
# ============================================================================
# File này chứa logic chính của hệ thống AI chatbox với RAG, LangChain, ChromaDB
# ============================================================================

import os
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from config import (
    CHROMA_DB_PATH, CHROMA_COLLECTION_NAME, CHROMA_HISTORY_COLLECTION,
    EMBEDDING_MODEL, EMBEDDING_DIMENSION, OPENAI_API_KEY, LLM_MODEL_NAME,
    LLM_TEMPERATURE, LLM_MAX_TOKENS, TOP_K_DOCUMENTS, SIMILARITY_THRESHOLD,
    CHUNK_SIZE, CHUNK_OVERLAP, SYSTEM_PROMPT, MAX_HISTORY_MESSAGES
)


class RAGSystem:
    """
    🤖 LỚP HỆ THỐNG RAG CHÍNH
    
    Quản lý:
    1. Tải và xử lý tài liệu (chunking)
    2. Tạo embedding (chuyển văn bản thành vector)
    3. Lưu vào ChromaDB
    4. Truy vấn và sinh câu trả lời
    5. Lưu lịch sử chat
    """
    
    def __init__(self):
        """
        ⚙️ KHỞI TẠO HỆ THỐNG RAG
        
        Công việc:
        1. Khởi tạo Embedding model (sentence-transformers)
        2. Kết nối ChromaDB
        3. Khởi tạo LLM (OpenAI)
        4. Tạo RAG chain
        """
        print("📚 Đang khởi tạo hệ thống RAG...")
        
        # ✅ BƯỚC 1: Khởi tạo Embedding model
        # 📌 embedding model chuyển các đoạn văn bản thành vector số (384 chiều)
        # Lợi ích: Có thể tính độ tương tự giữa các văn bản
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL,  # 📌 THAM SỐ: Model embedding
                model_kwargs={'device': 'cpu'}  # 📌 Dùng CPU (hoặc 'cuda' nếu có GPU)
            )
            print(f"✅ Embedding model tải thành công: {EMBEDDING_MODEL}")
        except Exception as e:
            print(f"❌ Lỗi tải embedding model: {e}")
            raise
        
        # ✅ BƯỚC 2: Kết nối ChromaDB
        # 📌 ChromaDB: Database vector lưu trữ document embeddings & lịch sử
        # Lợi ích: Nhanh chóng tìm kiếm semantic (ý nghĩa) thay vì từ khóa
        try:
            if not os.path.exists(CHROMA_DB_PATH):
                os.makedirs(CHROMA_DB_PATH)
            
            # Khởi tạo Chroma client
            self.chroma_client = chromadb.Client(Settings(
                chroma_db_impl_kwargs={"data_path": CHROMA_DB_PATH}
            ))
            print(f"✅ ChromaDB kết nối thành công: {CHROMA_DB_PATH}")
        except Exception as e:
            print(f"❌ Lỗi kết nối ChromaDB: {e}")
            raise
        
        # ✅ BƯỚC 3: Khởi tạo LangChain Chroma Vector Store
        # 📌 LangChain: Framework tích hợp LLM + vector store + chain
        # Lợi ích: Đơn giản hóa việc xây dựng RAG pipeline
        self.vector_store = Chroma(
            client=self.chroma_client,
            collection_name=CHROMA_COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=CHROMA_DB_PATH
        )
        print(f"✅ Vector store khởi tạo: {CHROMA_COLLECTION_NAME}")
        
        # ✅ BƯỚC 4: Khởi tạo LLM (Large Language Model)
        # 📌 OpenAI API: Model ngôn ngữ lớn để sinh phản hồi
        # Lợi ích: Khả năng hiểu và tạo văn bản tự nhiên
        try:
            self.llm = OpenAI(
                openai_api_key=OPENAI_API_KEY,  # 📌 THAM SỐ: API key OpenAI
                model_name=LLM_MODEL_NAME,  # 📌 THAM SỐ: gpt-3.5-turbo hoặc gpt-4
                temperature=LLM_TEMPERATURE,  # 📌 THAM SỐ: 0-1, 0=chính xác, 1=sáng tạo
                max_tokens=LLM_MAX_TOKENS,  # 📌 THAM SỐ: Độ dài tối đa phản hồi
            )
            print(f"✅ LLM khởi tạo: {LLM_MODEL_NAME}")
        except Exception as e:
            print(f"❌ Lỗi khởi tạo OpenAI LLM: {e}")
            raise
        
        # ✅ BƯỚC 5: Tạo RAG Chain (Chuỗi Retrieval-QA)
        # 📌 RAG Chain workflow:
        #    1. Câu hỏi → Embedding
        #    2. Tìm kiếm các tài liệu tương tự từ ChromaDB (semantic search)
        #    3. Gắn tài liệu vào prompt + câu hỏi gốc
        #    4. Gửi tới LLM để sinh phản hồi
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",  # 📌 chain_type: "stuff" = gộp tài liệu vào prompt
            retriever=self.vector_store.as_retriever(
                search_kwargs={
                    "k": TOP_K_DOCUMENTS,  # 📌 THAM SỐ: Số tài liệu lấy ra (5, 10, ...)
                    "filter": None  # 📌 Có thể thêm filter nếu muốn
                }
            ),
            return_source_documents=True  # 📌 Trả về tài liệu nguồn được sử dụng
        )
        print("✅ RAG Chain khởi tạo thành công")
        
        # ✅ BƯỚC 6: Khởi tạo Text Splitter (chia nhỏ tài liệu)
        # 📌 Lý do: Tài liệu lớn cần chia thành chunks nhỏ để xử lý
        # Lợi ích: Cải thiện độ chính xác của tìm kiếm
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,  # 📌 THAM SỐ: Kích thước mỗi chunk (500, 800, ...)
            chunk_overlap=CHUNK_OVERLAP,  # 📌 THAM SỐ: Độ trùng lặp (100, 200, ...)
            separators=["\n\n", "\n", " ", ""]  # 📌 Ưu tiên chia tại những ký tự này
        )
        print(f"✅ Text splitter khởi tạo: chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP}")
        
        # ✅ BƯỚC 7: Khởi tạo Collection lưu lịch sử chat
        # 📌 Collection riêng để lưu thông tin cuộc hội thoại
        # Lợi ích: Dễ dàng truy vấn lịch sử chat sau này
        self.history_collection = self.chroma_client.get_or_create_collection(
            name=CHROMA_HISTORY_COLLECTION,
            metadata={"hnsw:space": "cosine"}  # 📌 metric: cosine (tính độ tương tự)
        )
        print(f"✅ History collection khởi tạo: {CHROMA_HISTORY_COLLECTION}")
        print("=" * 60)
        print("🎉 Hệ thống RAG khởi tạo HOÀN THÀNH!")
        print("=" * 60)
    
    def add_documents(self, documents: List[str], metadata_list: Optional[List[Dict]] = None):
        """
        📄 THÊM TÀI LIỆU VÀO HỆ THỐNG
        
        Tham số:
        - documents (list): Danh sách tài liệu cần thêm
        - metadata_list (list): Thông tin metadata của từng tài liệu (source, author, ...)
        
        Quy trình:
        1. Chia nhỏ tài liệu thành chunks (đoạn nhỏ)
        2. Tạo embedding cho mỗi chunk
        3. Lưu vào ChromaDB
        
        💡 TỰ ĐỘNG HÓA ĐỂ AI THÔNG MINH HƠN:
        - Chỉnh CHUNK_SIZE nhỏ hơn (300) → chi tiết, chuẩn xác hơn
        - Chỉnh CHUNK_OVERLAP cao hơn (200) → giữ ngữ cảnh tốt hơn
        """
        try:
            print(f"\n📥 Đang xử lý {len(documents)} tài liệu...")
            
            all_splits = []  # Lưu tất cả chunks
            
            # ✅ Bước 1: Chia nhỏ mỗi tài liệu
            for idx, doc in enumerate(documents):
                if not doc or not doc.strip():
                    print(f"⚠️  Tài liệu {idx} trống, bỏ qua")
                    continue
                
                # Chia tài liệu thành chunks
                splits = self.text_splitter.split_text(doc)
                
                # Gắn metadata nếu có
                if metadata_list and idx < len(metadata_list):
                    for split in splits:
                        all_splits.append(Document(
                            page_content=split,
                            metadata={
                                **metadata_list[idx],
                                "source_index": idx
                            }
                        ))
                else:
                    for split in splits:
                        all_splits.append(Document(
                            page_content=split,
                            metadata={"source_index": idx}
                        ))
            
            # ✅ Bước 2: Thêm vào vector store
            print(f"📊 Tạo embedding cho {len(all_splits)} chunks...")
            
            # Thêm documents vào ChromaDB
            if all_splits:
                # Chuyển đổi Document objects thành format mà Chroma chấp nhận
                texts = [doc.page_content for doc in all_splits]
                metadatas = [doc.metadata for doc in all_splits]
                ids = [f"doc_{i}" for i in range(len(texts))]
                
                self.vector_store.add_texts(
                    texts=texts,
                    metadatas=metadatas,
                    ids=ids
                )
                
                print(f"✅ Thêm {len(all_splits)} chunks vào ChromaDB thành công!")
            else:
                print("⚠️  Không có chunks hợp lệ để thêm")
        
        except Exception as e:
            print(f"❌ Lỗi khi thêm tài liệu: {e}")
            raise
    
    def query(self, question: str, user_id: str = "default") -> Dict:
        """
        💬 TRẢ LỜI CÂU HỎI SỬ DỤNG RAG
        
        Tham số:
        - question (str): Câu hỏi từ người dùng
        - user_id (str): ID người dùng (để lưu lịch sử riêng biệt)
        
        Quy trình RAG:
        1. Chuyển câu hỏi thành vector embedding
        2. Tìm kiếm tài liệu tương tự nhất từ ChromaDB (semantic search)
        3. Lọc theo ngưỡng độ tương tự (SIMILARITY_THRESHOLD)
        4. Gắn tài liệu vào prompt + câu hỏi
        5. Gửi tới LLM để sinh phản hồi
        
        💡 TỰ ĐỘNG HÓA ĐỂ AI TỐT HƠN:
        - Tăng TOP_K_DOCUMENTS (5→10) → tìm kiếm kỹ hơn
        - Giảm SIMILARITY_THRESHOLD (0.5→0.3) → linh hoạt hơn
        - Giảm LLM_TEMPERATURE (0.7→0.3) → chính xác hơn
        """
        try:
            print(f"\n🔍 Xử lý câu hỏi: '{question}'")
            
            # ✅ Bước 1: Tìm kiếm tài liệu tương tự (RAG retrieval)
            # 📌 Semantic search: Tìm những tài liệu có ý nghĩa tương tự
            results = self.vector_store.similarity_search_with_scores(
                question,
                k=TOP_K_DOCUMENTS  # 📌 THAM SỐ: Lấy top-5 tài liệu tương tự
            )
            
            # ✅ Bước 2: Lọc theo ngưỡng độ tương tự
            # 📌 SIMILARITY_THRESHOLD: Chỉ sử dụng tài liệu đủ tương tự
            # Nếu không đủ tương tự → AI sẽ phản hồi "không tìm thấy"
            relevant_docs = []
            for doc, score in results:
                similarity = 1 - score  # Chuyển score → similarity (0-1)
                if similarity >= SIMILARITY_THRESHOLD:  # 📌 THAM SỐ: 0.5 (50% tương tự)
                    relevant_docs.append({
                        "content": doc.page_content,
                        "similarity": similarity,
                        "metadata": doc.metadata
                    })
            
            print(f"📚 Tìm được {len(relevant_docs)} tài liệu tương tự")
            
            # ✅ Bước 3: Sinh phản hồi sử dụng LLM
            # 📌 LLM nhận: tài liệu + câu hỏi + system prompt
            # Sau đó: Sinh phản hồi tự nhiên
            if relevant_docs:
                # Tạo context từ các tài liệu tương tự
                context = "\n---\n".join([doc["content"] for doc in relevant_docs])
                prompt = f"{SYSTEM_PROMPT}\n\nTài liệu:\n{context}\n\nCâu hỏi: {question}"
                
                # Gọi LLM để sinh phản hồi
                response = self.llm.predict(prompt)
            else:
                # Không tìm thấy tài liệu tương tự
                response = "Xin lỗi, tôi không tìm thấy thông tin liên quan trong cơ sở dữ liệu. Vui lòng thử câu hỏi khác hoặc cung cấp thêm tài liệu."
            
            # ✅ Bước 4: Lưu vào lịch sử chat (ChromaDB)
            self._save_to_history(
                user_id=user_id,
                question=question,
                answer=response,
                relevant_docs=relevant_docs
            )
            
            # ✅ Bước 5: Trả về kết quả
            return {
                "question": question,
                "answer": response,
                "relevant_documents": relevant_docs,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            print(f"❌ Lỗi khi trả lời câu hỏi: {e}")
            return {
                "question": question,
                "answer": f"❌ Lỗi: {str(e)}",
                "relevant_documents": [],
                "timestamp": datetime.now().isoformat()
            }
    
    def _save_to_history(self, user_id: str, question: str, answer: str, relevant_docs: List[Dict]):
        """
        💾 LƯU LỰC SỬ CHAT VÀO CHROMADB
        
        Tham số:
        - user_id: ID người dùng
        - question: Câu hỏi
        - answer: Câu trả lời
        - relevant_docs: Danh sách tài liệu được sử dụng
        
        Lợi ích:
        - Lưu lịch sử: Có thể truy vấn lại sau này
        - Phân tích: Biết được user thường hỏi gì
        - Cải thiện: Dùng feedback để fine-tune AI
        """
        try:
            history_entry = {
                "user_id": user_id,
                "question": question,
                "answer": answer,
                "num_relevant_docs": len(relevant_docs),
                "timestamp": datetime.now().isoformat()
            }
            
            # Lưu vào ChromaDB history collection
            entry_id = f"history_{user_id}_{int(datetime.now().timestamp() * 1000)}"
            
            self.history_collection.add(
                ids=[entry_id],
                documents=[question],  # 📌 Lưu câu hỏi để có thể tìm kiếm
                metadatas=[{
                    "user_id": user_id,
                    "answer": answer,
                    "timestamp": history_entry["timestamp"],
                    "num_relevant_docs": str(len(relevant_docs))
                }]
            )
        except Exception as e:
            print(f"⚠️  Lỗi khi lưu lịch sử: {e}")
            # Không raise exception, tiếp tục hoạt động
    
    def get_history(self, user_id: str, limit: int = MAX_HISTORY_MESSAGES) -> List[Dict]:
        """
        📜 LẤY LỊCH SỬ CHAT CỦA NGƯỜI DÙNG
        
        Tham số:
        - user_id: ID người dùng
        - limit: Số tin nhắn tối đa (📌 THAM SỐ: 20 mặc định)
        
        Trả về:
        - Danh sách các cuộc hội thoại gần đây
        """
        try:
            # Truy vấn từ ChromaDB history collection
            results = self.history_collection.get(
                where={"user_id": user_id},
                limit=limit
            )
            
            history = []
            for idx, doc_id in enumerate(results.get("ids", [])):
                metadatas = results.get("metadatas", [])[idx]
                documents = results.get("documents", [])[idx]
                
                history.append({
                    "question": documents,
                    "answer": metadatas.get("answer", ""),
                    "timestamp": metadatas.get("timestamp", ""),
                    "num_relevant_docs": int(metadatas.get("num_relevant_docs", 0))
                })
            
            return history
        
        except Exception as e:
            print(f"⚠️  Lỗi khi lấy lịch sử: {e}")
            return []
    
    def clear_documents(self):
        """
        🗑️  XÓA TẤT CẢ TÀI LIỆU TỪ VECTOR STORE
        
        Cảnh báo: Không thể khôi phục!
        """
        try:
            # Xóa và tạo lại collection
            self.chroma_client.delete_collection(CHROMA_COLLECTION_NAME)
            self.vector_store = Chroma(
                client=self.chroma_client,
                collection_name=CHROMA_COLLECTION_NAME,
                embedding_function=self.embeddings,
                persist_directory=CHROMA_DB_PATH
            )
            print("✅ Xóa tất cả tài liệu thành công")
        except Exception as e:
            print(f"❌ Lỗi khi xóa tài liệu: {e}")
    
    def get_stats(self) -> Dict:
        """
        📊 LẤY THỐNG KÊ VỀ HỆ THỐNG
        
        Trả về:
        - Số lượng tài liệu
        - Số lượng chunks
        - Model sử dụng
        - ...
        """
        try:
            count = self.vector_store._collection.count()
            return {
                "total_documents": count,
                "embedding_model": EMBEDDING_MODEL,
                "llm_model": LLM_MODEL_NAME,
                "chroma_path": CHROMA_DB_PATH,
                "chunk_size": CHUNK_SIZE,
                "top_k": TOP_K_DOCUMENTS,
                "similarity_threshold": SIMILARITY_THRESHOLD
            }
        except Exception as e:
            print(f"❌ Lỗi khi lấy thống kê: {e}")
            return {}


# ============================================================================
# FUNCTIONS HỖ TRỢ
# ============================================================================

def load_text_file(file_path: str) -> Optional[str]:
    """
    📄 TẢI TÀI LIỆU TỪ FILE TEXT
    
    Tham số:
    - file_path: Đường dẫn file
    
    Trả về:
    - Nội dung text hoặc None nếu lỗi
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Lỗi khi đọc file {file_path}: {e}")
        return None


def load_multiple_files(directory: str, file_pattern: str = "*.txt") -> List[str]:
    """
    📁 TẢI NHIỀU TÀI LIỆU TỪ THƯ MỤC
    
    Tham số:
    - directory: Đường dẫn thư mục
    - file_pattern: Pattern file (*.txt, *.md, ...)
    
    Trả về:
    - Danh sách nội dung file
    """
    import glob
    
    documents = []
    try:
        files = glob.glob(os.path.join(directory, file_pattern))
        for file_path in files:
            content = load_text_file(file_path)
            if content:
                documents.append(content)
                print(f"✅ Tải: {os.path.basename(file_path)}")
    except Exception as e:
        print(f"❌ Lỗi khi tải thư mục: {e}")
    
    return documents

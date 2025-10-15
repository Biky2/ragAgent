import os
import faiss
import numpy as np
import pickle
from typing import List, Any
from sentence_transformers import SentenceTransformer
from src.embedding import EmbeddingPipeline
from src.dataloader import load_data
class faissvectordb:
    def __init__(self,persist_dir:str="faiss_index",embedding_model:str="all-MiniLM-L6-v2",chunk_size: int = 1000, chunk_overlap: int = 200):
        self.persist_dir=persist_dir
        os.makedirs(self.persist_dir,exist_ok=True)
        self.embedding_model=embedding_model
        self.model=SentenceTransformer(self.embedding_model)

        self.chunk_size=chunk_size
        self.chunk_overlap=chunk_overlap
        # self.emb_pipe=EmbeddingPipeline(model_name=self.embedding_model,chunk_size=self.chunk_size,chunk_overlap=self.chunk_overlap)
        self.index=None
        self.metadata=[]
        print(f"Loaded embedding model {self.embedding_model}")
        
    def build_from_docu(self,documents:List[Any]):
        print("Building FAISS vector store from documents...")
        embd=EmbeddingPipeline(model_name=self.embedding_model,chunk_size=self.chunk_size,chunk_overlap=self.chunk_overlap)
        texts=embd.chunk_documents(documents)
        embeddings=embd.embd_texts(texts)
        metadata=[{"text":t.page_content} for t in texts
                  ]
        self.add_embeddimgs(np.array(embeddings).astype("float32"),metadata )
        print("FAISS vector store built and saved.")
        self.save()
        print(f"FAISS index saved to {self.persist_dir}")   
        
    def add_embeddimgs(self,embeddings:np.ndarray,metadata:List[dict]):
        if self.index is None:
            dim=embeddings.shape[1]
            self.index=faiss.IndexFlatL2(dim)  #FOR SEARCHING SMILIARTY
            print(f"Created new FAISS index with dimension {dim}")
        self.index.add(embeddings)
        self.metadata.extend(metadata)
        print(f"Added {len(embeddings)} embeddings to the index. Total embeddings: {self.index.ntotal}")
    
    def save(self):
        faiss_path=os.path.join(self.persist_dir,"faiss_index.bin")
        meta_path=os.path.join(self.persist_dir,"metadata.pkl")
        faiss.write_index(self.index,faiss_path)
        with open(meta_path,"wb") as f:
            pickle.dump(self.metadata,f)
        print(f"FAISS index and metadata saved to {self.persist_dir}")
        
    def load(self):
        faiss_path=os.path.join(self.persist_dir,"faiss_index.bin")
        meta_path=os.path.join(self.persist_dir,"metadata.pkl")
        if os.path.exists(faiss_path) and os.path.exists(meta_path):
            self.index=faiss.read_index(faiss_path)
            with open(meta_path,"rb") as f:
                self.metadata=pickle.load(f)
            print(f"Loaded FAISS index with {self.index.ntotal} embeddings from {self.persist_dir}")
        else:
            print("FAISS index or metadata file not found. Please build the index first.")
            
    # def search(self,query:str,top_k:int=5)->List[dict]:
    #     if self.index is None:
    #         raise ValueError("FAISS index is not loaded. Please load or build the index first.")
    #     query_embd=self.model.encode([query]).astype("float32")
    #     D,I=self.index.search(query_embd,top_k)
    #     results=[]
    #     for idx, dist in zip(I[0], D[0]):
    #         meta = self.metadata[idx] if idx < len(self.metadata) else None
    #         results.append({"index": idx, "distance": dist, "metadata": meta})
    #     return results
    
    # def quwey(self,query:str,top_k:int=5):
        
    #     pass
    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        D, I = self.index.search(query_embedding, top_k)
        results = []
        for idx, dist in zip(I[0], D[0]):
            meta = self.metadata[idx] if idx < len(self.metadata) else None
            results.append({"index": idx, "distance": dist, "metadata": meta})
        return results

    def query(self, query_text: str, top_k: int = 5):
        print(f"[INFO] Querying vector store for: '{query_text}'")
        query_emb = self.model.encode([query_text]).astype('float32')
        return self.search(query_emb, top_k=top_k)


if __name__ == "__main__":
  
    docs = load_data("data")
    store =faissvectordb("faiss_store")
    store.build_from_documents(docs)
    store.load()
    print(store.query("What is attention mechanism?", top_k=3))


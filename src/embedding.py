from typing import List,Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
from src.dataloader import load_data


class EmbeddingPipeline:
    def __init__(self,model_name:str="all-MiniLM-L6-v2",chunk_size:int=1000,chunk_overlap:int=200):
        self.chunk_size=chunk_size
        self.chunk_overlap=chunk_overlap
        self.model=SentenceTransformer(model_name)
        print(f"Loaded embedding model {model_name}")
        
    def chunk_documents(self,documents:List[Any])->List[str]:
        splitter=RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n","\n",".","!","?"," ", ""]
            
        )
        texts=splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(texts)} chunks")
        return texts
    def embd_texts(self,texts:List[str])->np.ndarray:
        embeddings=self.model.encode([t.page_content for t in texts],show_progress_bar=True)
        print(f"Generated embeddings for {len(texts)} texts")
        return embeddings
    
    
if __name__ == "__main__":
    
    docs = load_data("data")
    emb_pipe = EmbeddingPipeline()
    chunks = emb_pipe.chunk_documents(docs)
    embeddings = emb_pipe.embd_texts(chunks)
    print("[INFO] Example embedding:", embeddings[0] if len(embeddings) > 0 else None)
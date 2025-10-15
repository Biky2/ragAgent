
from src.dataloader import load_data as load_all_documents
from src.seach import  RAGSearch
from src.vectordb import faissvectordb as FaissVectorStore

if __name__ == "__main__":
    
    docs = load_all_documents("src/OceanofPDF.com_The_Art_of_Persuasion_-_Bob_Burg.pdf")
    store = FaissVectorStore("faiss_store")
    #store.build_from_documents(docs)
    store.load()
    #print(store.query("What is attention mechanism?", top_k=3))
    rag_search = RAGSearch()
    query = "The Role Our Egos Play"
    summary = rag_search.search_and_summarize(query, top_k=3)
    print("Summary:", summary)
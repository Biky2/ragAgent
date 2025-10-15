# from pathlib import Path
# from typing import List,Any
# from langchain_community.document_loaders import PyPDFLoader,TextLoader,CSVLoader
# from langchain_community.document_loaders import Docx2txtLoader,UnstructuredExcelLoader,json_loader

# def load_data(file:str)->List[Any]:
#     # load data from file
#     data_path=Path(file).resolve()
#     print(f"Loading data from {data_path}")
#     if not data_path.exists():
#         raise FileNotFoundError(f"File {data_path} does not exist") 
#     documents=[]
    
#     # pdf files
#     pdf_files=list(data_path.glob("**/*.pdf"))
#     print(f"Found {len(pdf_files)} pdf files")
#     for pdf_file in pdf_files:
#         print(f"[debug] Loading pdf file {pdf_file} ")
#         try:
#             loader=PyPDFLoader(str(pdf_file))
#             documents.extend(loader.load())
#         except Exception as e:
#             print(f"Error loading pdf file {pdf_file}: {e}")
#     print(f"Loaded {len(documents)} documents from pdf files")
    
    
    
#      # text files
#     text_files=list(data_path.glob("**/*.txt"))
#     print(f"Found {len(text_files)} pdf files")
#     for text_file in text_files:
#         print(f"[debug] Loading pdf file {text_file} ")
#         try:
#             loader=TextLoader(str(text_file))
#             documents.extend(loader.load())
#         except Exception as e:
#             print(f"Error loading pdf file {text_file}: {e}")
#     print(f"Loaded {len(documents)} documents from pdf files")
    
    
    
#      # scv files
#     csv_files=list(data_path.glob("**/*.csv"))
#     print(f"Found {len(csv_files)} pdf files")
#     for csv_file in csv_files:
#         print(f"[debug] Loading pdf file {csv_file} ")
#         try:
#             loader=CSVLoader(str(csv_file))
#             documents.extend(loader.load())
#         except Exception as e:
#             print(f"Error loading pdf file {csv_file}: {e}")
#     print(f"Loaded {len(documents)} documents from pdf files")
    
    
    
#      # excel files
#     excel_files=list(data_path.glob("**/*.xlsx"))
#     print(f"Found {len(excel_files)} pdf files")
#     for pdf_file in excel_files:
#         print(f"[debug] Loading pdf file {pdf_file} ")
#         try:
#             loader=UnstructuredExcelLoader(str(pdf_file))
#             documents.extend(loader.load())
#         except Exception as e:
#             print(f"Error loading pdf file {pdf_file}: {e}")
#     print(f"Loaded {len(documents)} documents from pdf files")
    
#      # word files
#     pdf_files=list(data_path.glob("**/*.docx"))
#     print(f"Found {len(pdf_files)} pdf files")
#     for pdf_file in pdf_files:
#         print(f"[debug] Loading pdf file {pdf_file} ")
#         try:
#             loader=Docx2txtLoader(str(pdf_file))
#             documents.extend(loader.load())
#         except Exception as e:
#             print(f"Error loading pdf file {pdf_file}: {e}")
#     print(f"Loaded {len(documents)} documents from pdf files")
    
    
    
#      # json files
#     pdf_files=list(data_path.glob("**/*.json"))
#     print(f"Found {len(pdf_files)} pdf files")
#     for pdf_file in pdf_files:
#         print(f"[debug] Loading pdf file {pdf_file} ")
#         try:
#             loader=json_loader(str(pdf_file))
#             documents.extend(loader.load())
#         except Exception as e:
#             print(f"Error loading pdf file {pdf_file}: {e}")
#     print(f"Loaded {len(documents)} documents from pdf files")
    
    
#     print(f"Total loaded {len(documents)} documents")
#     return documents

# if __name__=="__main__":
#     docs=load_data("data")
#     print(f"Loaded {len(docs)} documents.")
#     print("Example document:", docs[0] if docs else None)



from pathlib import Path
from typing import List, Any
from langchain_community.document_loaders import (
    PyPDFLoader, TextLoader, CSVLoader,
    Docx2txtLoader, UnstructuredExcelLoader, json_loader
)

def load_data(file_or_folder: str) -> List[Any]:
    """
    Load documents from a single file or a folder.
    Supported file types: PDF, TXT, CSV, XLSX, DOCX, JSON.
    """
    data_path = Path(file_or_folder).resolve()
    print(f"Loading data from: {data_path}")

    if not data_path.exists():
        raise FileNotFoundError(f"File or folder {data_path} does not exist")

    documents: List[Any] = []

    # Helper function to load a single file
    def load_file(file_path: Path):
        ext = file_path.suffix.lower()
        loader = None
        try:
            if ext == ".pdf":
                loader = PyPDFLoader(str(file_path))
            elif ext == ".txt":
                loader = TextLoader(str(file_path))
            elif ext == ".csv":
                loader = CSVLoader(str(file_path))
            elif ext == ".xlsx":
                loader = UnstructuredExcelLoader(str(file_path))
            elif ext == ".docx":
                loader = Docx2txtLoader(str(file_path))
            elif ext == ".json":
                loader = json_loader(str(file_path))
            else:
                print(f"⚠ Skipping unsupported file type: {file_path}")
                return

            loaded_docs = loader.load()
            documents.extend(loaded_docs)
            print(f"✅ Loaded {len(loaded_docs)} document(s) from {file_path}")
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")

    if data_path.is_file():
        # Single file
        load_file(data_path)
    else:
        # Folder: iterate all supported files
        supported_exts = ["*.pdf", "*.txt", "*.csv", "*.xlsx", "*.docx", "*.json"]
        for ext in supported_exts:
            for file_path in data_path.glob(f"**/{ext}"):
                load_file(file_path)

    print(f"\nTotal loaded documents: {len(documents)}")
    return documents


if __name__ == "__main__":
    # Example usage
    docs = load_data("data/OceanofPDF.com_The_Art_of_Persuasion_-_Bob_Burg.pdf")  # single file
    # docs = load_data("data")  # folder
    print(f"Example document: {docs[0] if docs else None}")

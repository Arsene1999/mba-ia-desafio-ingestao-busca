import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
CONNECTION = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")

embeddings = OpenAIEmbeddings()

def ingest_pdf():
    print(f"Lendo o arquivo: {PDF_PATH}...")
    
    loader = PyPDFLoader(PDF_PATH)
    documentos_inteiros = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100
    )
    meus_chunks_de_texto = text_splitter.split_documents(documentos_inteiros)
    
    print(f"Criados {len(meus_chunks_de_texto)} chunks de texto.")

    print("Iniciando o processo de ingestão no PGVector...")
    
    vector_store = PGVector.from_documents(
        documents=meus_chunks_de_texto,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION,
        use_jsonb=True
    )
    
    print("Tabelas verificadas/criadas e dados inseridos com sucesso!")

if __name__ == "__main__":
    ingest_pdf()
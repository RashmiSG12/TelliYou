
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
import os
import shutil

CHROMA_DB_ROOT = "chroma_db"

def split_transcript(transcript: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_text(transcript)
    return [Document(page_content=chunk) for chunk in chunks]

def create_vectorstore(chunks, video_id):
    persist_directory = os.path.join(CHROMA_DB_ROOT, video_id)

    if os.path.exists(persist_directory):
        try:
            shutil.rmtree(persist_directory, ignore_errors=True)
            print(f"🧹 Old ChromaDB folder deleted for video: {video_id}")
        except Exception as e:
            print(f"❌ Error deleting old ChromaDB folder: {e}")    

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectorstore.persist()
    print(f"✅ Vectorstore created and persisted for video: {video_id}")

    return vectorstore

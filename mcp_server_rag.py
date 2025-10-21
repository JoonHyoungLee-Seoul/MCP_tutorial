from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Any
import os

load_dotenv(override=True)

# OPENAI_BASE_URL이 시스템 환경변수에 Fireworks AI로 설정되어 있는 경우 제거
# OpenAI Embeddings가 정상적으로 작동하도록 함
if 'OPENAI_BASE_URL' in os.environ:
    del os.environ['OPENAI_BASE_URL']

# 전역 변수로 retriever 저장 (한 번만 초기화)
_retriever = None

def create_retriever() -> Any:
    """
    Creates and returns a document retriever based on FAISS vector store.
    
    This function performs the following steps:
    1. Loads a PDF document(place your PDF file in the data folder)
    2. Splits the document into manageable chunks
    3. Creates embeddings for each chunk
    4. Builds a FAISS vector store from the embeddings
    5. Returns a retriever interface to the vector store
    
    Returns:
        Any: A retriever object that can be used to query the document database
    """
    
    # Step 1: Load Documents
    # DirectoryLoader is used to load all PDF files from a directory
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    loader = DirectoryLoader(
        data_dir,
        glob="**/*.pdf",
        loader_cls=PyMuPDFLoader,
        show_progress=False  # stdio 방식에서는 진행률 출력 비활성화
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} documents from {data_dir}")
    
    # Step 2: Split Documents
    # Recursive splitter divides documents into chunks with some overlap to maintain context
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    split_documents = text_splitter.split_documents(docs)
    
    # Step 3: Create Embeddings
    # OpenAI's text=embedding-small-3-small model used to convert text chunks into vector embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # Step 4: Create Vector Database
    # FAISS is an efficient similarity search library that stores vector embeddings
    # and allows for fast retrieval of similar vectors
    vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)
    
    # Step 5: Create Retriever
    # The retriever provides an interface to search the vector database
    # and retrieve documents relevant to a query
    retriever = vectorstore.as_retriever()
    return retriever

# Initialize FastMCP server with configuration
mcp = FastMCP(
    "Retriever",
    instructions="A Retriever that can retrieve information from the database.",
    host="0.0.0.0",
    port=8005,
)
    
    
@mcp.tool()
async def retrieve(query: str) -> str:
    """
    Retrieves information from the document database based on the query.

    This function creates a retriever, queries it with the provided input,
    and returns the concatenated content of all retrieved documents.

    Args:
        query (str): The search query to find relevant information

    Returns:
        str: Concatenated text content from all retrieved documents
    """
    global _retriever

    # 한 번만 retriever 생성 (캐싱)
    if _retriever is None:
        print("Initializing retriever for the first time...")
        _retriever = create_retriever()
        print("Retriever initialized successfully!")

    # Use invoke() method to get relevant documents based on the query
    retrieved_docs = _retriever.invoke(query)

    # Join all document contents with newlines and return as a single string
    return "\n".join([doc.page_content for doc in retrieved_docs])

if __name__ == "__main__":
    mcp.run(transport="stdio")
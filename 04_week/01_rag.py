from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os 
from dotenv import load_dotenv

load_dotenv()

pdf_path = Path(__file__).parent/"WSFSE.pdf"
loader = PyPDFLoader(pdf_path)
docs = loader.load()

# print(docs)
# print(docs[21])
# print(docs[0].metadata)

docs_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
docs_split = docs_splitter.split_documents(docs)

print("docs length: ", len(docs))
print("split docs lenght: ", len(docs_split))


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


vector_store = QdrantVectorStore.from_documents(
    documents=[],
    url="http://localhost:6333",
    collection_name="learning_langchain",
    embedding=embeddings
)

# vector_store = QdrantVectorStore.from_documents(
#     documents=[],
#     url="http://localhost:6333",
#     collection_name="learning RAG",
#     embedding=embeddings,
# )

# vector_store.add_documents(documents=docs_split)
print("Ingestion done!")

retriever = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning RAG",
    embedding=embeddings
)

responses = retriever.similarity_search(
    query="what is CDN ?"
)

print("Relevent Response: ",responses)
page_contents = [doc.page_content for doc in responses]
print(page_contents)

for content in page_contents:
    print(content)
    print("=" * 150)  # Separator between pages

# from pathlib import Path
# from langchain_docling import DoclingLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# pdf_path = Path(__file__).parent / "Shear strength notes.pdf"

# loader = DoclingLoader(file_path=pdf_path)


# for document in loader.lazy_load():
#     print(document)




from pathlib import Path
from langchain_docling import DoclingLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import AzureOpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
import getpass
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage



load_dotenv()
pdf_path = Path(__file__).parent / "Shear strength notes.pdf"

loader = DoclingLoader(file_path=pdf_path)

documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0
)

texts = text_splitter.split_documents(documents)

# print(texts)


# if not os.environ.get("AZURE_OPENAI_API_KEY"):
#     os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass("Enter API key for Azure: ")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded")

llm = ChatGroq(
    model="openai/gpt-oss-120b",  # or whichever Groq model you want
    groq_api_key=os.environ["GROQ_API_KEY"],
)

qdrant_url = "http://localhost:6333"

collection_name = "shear_strength_notes"


# -----------------------------------
# 7. Store chunks + embeddings
# -----------------------------------

vector_store = QdrantVectorStore.from_documents(
    documents=texts,
    embedding=embeddings,
    url=qdrant_url,
    collection_name=collection_name,
)

# print("Successfully stored documents in Qdrant!")
user_query = input("Ask something: ")

search_results = vector_store.similarity_search(query=user_query)


context = "\n\n".join(
    document.page_content
    for document in search_results
)


SYSTEM_PROMPT = f"""
 You are a helpfull AI assistant who answers user quer based on the available context
 retrived from a PDF file along with page_contaents and pagee number.

 You should only ans the user based on the following context and navigate the user to
 open the right page number to know more.

 Context:
 {context}
"""

response = llm.invoke([
    SystemMessage(content=SYSTEM_PROMPT),
    HumanMessage(content=user_query),
])
print("\nGrok Answer:")
print(response.content)
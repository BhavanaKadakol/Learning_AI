from pathlib import Path
from langchain_docling import DoclingLoader
pdf_path = Path(__file__).parent / "Shear strength notes.pdf"

loader = DoclingLoader(file_path=pdf_path)

documents = loader.load()

for document in loader.lazy_load():

    print(document)


# Load all documents
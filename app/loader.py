# app/loader.py

import logging
from pathlib import Path
from langchain_community.document_loaders import TextLoader, CSVLoader, PyMuPDFLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_null_bytes(text: str) -> str:
    """Replace null bytes in text."""
    return text.replace("\x00", "")

def chunk_documents(docs, chunk_size=500, chunk_overlap=50):
    """Splits documents into smaller chunks and cleans null bytes."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(docs)
    for chunk in chunks:
        chunk.page_content = clean_null_bytes(chunk.page_content)
    return chunks


def load_documents_from_folder(folder_path: str, dataset_tag: str = "default") -> list[Document]:
    """Loads all supported files from a folder and tags them with metadata."""
    docs = []
    logger.info(f"[LOADER] Loading files from folder: {folder_path}")
    
    for path in Path(folder_path).rglob("*"):
        if path.is_file():
            logger.info(f"[LOADER] Processing file: {path}")
            try:
                # Choose loader based on file extension
                if path.suffix == ".txt":
                    loader = TextLoader(path.as_posix())
                elif path.suffix == ".csv":
                    loader = CSVLoader(path.as_posix())
                elif path.suffix == ".pdf":
                    loader = PyMuPDFLoader(path.as_posix())
                else:
                    logger.warning(f"[SKIP] Unsupported file: {path}")
                    continue

                # Load document
                loaded_docs = loader.load()
                
                # Clean content + add metadata
                tagged_docs = [
                    Document(
                        page_content=clean_null_bytes(doc.page_content),
                        metadata={**doc.metadata, "dataset": dataset_tag}
                    )
                    for doc in loaded_docs
                ]
                docs.extend(tagged_docs)

            except Exception as e:
                logger.error(f"[ERROR] Failed to load {path}: {e}")

    logger.info(f"[LOADER] Total documents loaded: {len(docs)}")
    return docs


if __name__ == "__main__":
    import os
    from pprint import pprint

    folder_path = os.path.join("..", "data")
    docs = load_documents_from_folder(folder_path, dataset_tag="sample_data")

    print(f"[TEST] Loaded {len(docs)} documents")

    for i, doc in enumerate(docs[:3]):
        print(f"\n--- Document {i+1} ---")
        pprint(doc.page_content[:500])
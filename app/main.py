# app/main.py

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from loader import load_documents_from_folder, chunk_documents
from vector_store import get_pg_vectorstore, store_chunks
from rag_engine import query_rag
import uvicorn
import os

app = FastAPI(
    title="RAG FastAPI Service",
    description="Load data into embeddings & query via local LLM",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup vector DB connection
vectorstore = get_pg_vectorstore()

# Endpoint to load all documents from "data/" and embed + store in DB
@app.post("/load-data")
def load_data(dataset: str = "default"):
    docs = load_documents_from_folder("data/", dataset_tag=dataset)
    if not docs:
        return {"status": "No documents found."}
    
    chunks = chunk_documents(docs)
    store_chunks(chunks, vectorstore)
    return {
        "status": "Success",
        "docs_loaded": len(docs),
        "chunks_created": len(chunks),
        "dataset_tag": dataset
    }

# Endpoint to ask a question to the RAG system
@app.get("/ask")
def ask(
    question: str = Query(..., description="Your question to query the knowledge base"),
    dataset: str = Query(None, description="Optional dataset tag to filter results")
):
    answer = query_rag(question, vectorstore, dataset_filter=dataset)
    return {
        "question": question,
        "answer": answer,
        "dataset_used": dataset or "all"
    }


# Run directly with `python3 main.py`
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
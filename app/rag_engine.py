# app/rag_engine.py

import logging
from ollama_client import query_ollama

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def query_rag(question, vectorstore, dataset_filter=None):
    logger.info(f"[RAG] Querying RAG system for question: '{question}'")
    
    # Apply dataset filter if provided
    filter_dict = {"dataset": dataset_filter} if dataset_filter else None
    
    retrieved_docs = vectorstore.similarity_search(question, k=5, filter=filter_dict)
    
    context = "\n".join([doc.page_content for doc in retrieved_docs])
    prompt = f"Use the context below to answer the question:\n\n{context}\n\nQuestion: {question}"
    
    logger.info("[RAG] Sending prompt to LLM...")
    return query_ollama(prompt)
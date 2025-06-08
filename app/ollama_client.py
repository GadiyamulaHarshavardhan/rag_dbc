# app/ollama_client.py

import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = "http://localhost:11434/api/generate"

def query_ollama(prompt: str, model: str = "llama3"):
    logger.info(f"[OLLAMA] Using model: {model}")
    try:
        response = requests.post(
            OLLAMA_BASE_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        if response.status_code == 200:
            logger.info("[OLLAMA] Response received successfully.")
            return response.json()["response"].strip()
        else:
            logger.error(f"[OLLAMA] Returned status {response.status_code}: {response.text}")
            return f"[ERROR] Ollama returned status {response.status_code}: {response.text}"
    except Exception as e:
        logger.exception("[OLLAMA] Connection failed.")
        return f"[ERROR] Failed to connect to Ollama: {e}"
## 📚 Retrieval-Augmented Generation (RAG) FastAPI Service

A simple RAG system that uses **PostgreSQL + pgvector**, **LangChain**, **FastAPI**, and **Ollama** to load documents, store embeddings, and answer questions using a local LLM like `llama3`.

### 🧠 What This Project Does

- Loads `.txt`, `.csv`, and `.pdf` files from a folder
- Splits them into chunks
- Stores embeddings in PostgreSQL using `pgvector`
- Lets you ask questions via an API
- Uses a local LLM via [Ollama](https://ollama.ai)

---

## 🧰 Prerequisites

Before running this project, make sure you have:

- ✅ **Python 3.9+**
- ✅ **PostgreSQL** with `pgvector` extension
- ✅ **Ollama** installed and running locally
- ✅ A folder called `data/` with your PDFs, CSVs, or TXTs

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

If not already installed:
```bash
pip install python-dotenv
```

---

## 🗃️ Setup PostgreSQL

1. Create a new database:
   ```bash
   createdb rag_db
   ```

2. Enable the `vector` extension:
   ```bash
   psql -d rag_db -c "CREATE EXTENSION vector;"
   ```

---

## 📁 Prepare Your Data

Put all your `.txt`, `.csv`, and `.pdf` files in the `data/` folder:

```
rag_project/
├── data/
│   ├── document1.pdf
│   ├── notes.txt
│   └── sales.csv
├── app/
└── requirements.txt
```

---

## 🌐 Run the Server

```bash
cd rag_project
python app/main.py
```

Your API will be available at:

```
http://localhost:8000
```

Swagger UI (for testing):  
👉 http://localhost:8000/docs

---

## 🚀 How to Use

### 1. Load Documents into Vector Store

Send a POST request to `/load-data`:

```bash
curl -X POST "http://localhost:8000/load-data?dataset=my_dataset"
```

This loads all files from `data/`, splits them into chunks, and stores their embeddings in PostgreSQL.

---

### 2. Ask a Question

Query the RAG system:

```bash
curl "http://localhost:8000/ask?question=What+is+the+summary+of+file1&dataset=my_dataset"
```

It retrieves relevant context from your documents and generates an answer using the LLM.

---

## 🛠️ Optional: Set Environment Variables

Create a `.env` file:

```env
POSTGRES_CONNECTION=postgresql://postgres:password@localhost:5432/rag_db
```

Make sure to install `python-dotenv` if you use it.

---

## 🧪 Sample Output

After loading data:
```json
{
  "status": "Success",
  "docs_loaded": 10,
  "chunks_created": 120,
  "dataset_tag": "my_dataset"
}
```

After asking a question:
```json
{
  "question": "What is the summary of file1",
  "answer": "The document discusses...",
  "dataset_used": "my_dataset"
}
```

---

## 🧹 Reset Database (Optional)

To start fresh:

```bash
dropdb rag_db
createdb rag_db
psql -d rag_db -c "CREATE EXTENSION vector;"
```

Then reload your data.

---

## 📝 Requirements.txt

```txt
fastapi
uvicorn
langchain
langchain-community
pgvector
psycopg2-binary
requests
pydantic
python-dotenv
```

---

## 🙌 Want More?

Would you like help with:

- 🐳 Dockerizing this setup?
- 🖥️ Building a simple frontend?
- 🔐 Adding authentication?
- 📊 Viewing stored documents via an API?

Let me know — I'm happy to help!

---

Happy coding! 🚀  
Your RAG-powered search engine is now ready to go!

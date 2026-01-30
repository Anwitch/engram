# Engram Skill

**Engram** provides semantic search capabilities for a local knowledge base (e.g., an Obsidian vault) by leveraging Pinecone for vector storage and Google's Gemini for text embeddings.

It allows an AI agent to find relevant information based on conceptual meaning, not just keywords.

---

## Requirements

- A local folder containing Markdown files (your knowledge base).
- **Pinecone API Key**: For vector database storage.
- **Google Gemini API Key**: For generating text embeddings.

---

## Setup & Configuration

1.  **Install Dependencies**:
    ```bash
    cd /path/to/skills/engram
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Configure Environment**:
    Create a `.env` file in the skill's root directory (`engram/`) with the following content:
    ```ini
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    PINECONE_API_KEY="YOUR_PINECONE_API_KEY"
    PINECONE_HOST="YOUR_PINECONE_INDEX_HOST_URL"
    LOCAL_REPO_PATH="/path/to/your/markdown/knowledge_base"
    ```

3.  **Test Connection**:
    Run the test script to ensure all keys and paths are correct.
    ```bash
    python test_connection.py
    ```

---

## Usage

### Indexing

To build or update the search index, run the indexing tool. This process reads your markdown files, generates embeddings for text chunks, and upserts them into your Pinecone index.

```bash
python tool_engram_index.py
```
*It is recommended to run this periodically (e.g., via a cron job) to keep the search index synchronized with your notes.*

### Searching

To perform a search, use the search tool. It takes a JSON input with your query.

```bash
# Example JSON for search
echo '{"query": "What are my notes on system architecture?"}' | python tool_engram_search.py
```

The tool will return a JSON object containing the most relevant text snippets from your knowledge base based on semantic similarity.

---
*Skill created by Anwitch.*

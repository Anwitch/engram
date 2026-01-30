---
name: engram
description: Transform your Obsidian vault into searchable AI memory with semantic vector search and auto-indexing
homepage: https://github.com/Anwitch/engram
difficulty: advanced
metadata: 
  clawdbot:
    emoji: 🧠
    requires:
      bins: ["python3"]
      env: ["GEMINI_API_KEY", "PINECONE_API_KEY", "PINECONE_HOST", "LOCAL_REPO_PATH"]
    primaryEnv: "PINECONE_API_KEY"
    install:
      - id: pip
        kind: pip
        packages: ["google-genai>=1.0.0", "pinecone>=5.0.0", "python-dotenv>=1.0.0", "GitPython>=3.1.0"]
        label: "Install Python dependencies"
user-invocable: true
---

# 🧠 Engram - Semantic Memory System

> "A hypothetical permanent change in the brain accounting for the existence of memory; a memory trace."

**Transform your Obsidian vault into persistent, searchable AI memory.**

Perfect for power users who want their AI companion to remember everything from their personal knowledge base.

## ⚠️ Prerequisites

**Time to Setup:** 15-20 minutes  
**Technical Level:** Advanced  
**Monthly Cost:** $0-5 (free tier available)

**You will need:**
1. ✅ Obsidian vault or markdown knowledge base
2. ✅ [Gemini API key](https://aistudio.google.com/app/apikey) (free)
3. ✅ [Pinecone account](https://app.pinecone.io/) (free tier: 100K vectors)
4. ✅ Basic command line familiarity

**Recommended (Optional):**
- P.A.R.A. structured vault (Projects, Areas, Resources, Archive)
- Git repository for your vault

---

## 🎯 What This Does

Engram gives your AI companion **episodic memory**:

- **🔍 Semantic Search:** Natural language queries across your entire vault
- **📚 Auto-Indexing:** Daily re-indexing keeps memory fresh (cron job)
- **🏷️ Smart Metadata:** P.A.R.A. structure awareness, project tracking
- **🔗 Traceability:** Direct GitHub links to source files
- **🧠 Rich Context:** 768-dimensional embeddings for deep understanding

**Example queries:**
- "What did I learn about RAG systems?"
- "Show me all notes about project X"
- "How does topic A relate to topic B in my notes?"
- "Remember when I worked on PKM?"

---

## 🚀 Quick Start

### 1. Get API Keys

**Gemini API (Free):**
1. Visit https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key (starts with `AIzaSy...`)

**Pinecone API (Free tier available):**
1. Sign up at https://app.pinecone.io/
2. Create new index:
   - **Name:** `your-vault-name` (e.g., "rudybrain")
   - **Dimensions:** `768`
   - **Metric:** `cosine`
   - **Cloud:** `AWS` (free tier)
   - **Region:** `us-east-1`
3. Go to API Keys → Copy your API key (starts with `pcsk_...`)
4. Copy your index host URL (in index details page)

### 2. Configure Skill

Edit `.env` file in skill directory:

```bash
GEMINI_API_KEY=AIzaSy...your_key_here
PINECONE_API_KEY=pcsk_...your_key_here
PINECONE_HOST=https://your-index-name-xxxxx.svc.pinecone.io
LOCAL_REPO_PATH=/path/to/your/obsidian/vault
```

### 3. Test & Index

```bash
# Test connection
.venv/bin/python test_connection.py

# Run initial indexing (may take 1-2 minutes)
.venv/bin/python tool_engram_index.py
```

You should see:
```
✅ 46/46 chunks berhasil di-index
```

### 4. Try Searching

```bash
echo '{"query": "your question", "min_score": 0.3}' | .venv/bin/python tool_engram_search.py
```

---

## 🛠️ Tools

### engram_search

Search your knowledge base with semantic understanding.

**Parameters:**
- `query` (string, required): Natural language search query
- `top_k` (number, default: 5): Number of results (max 20)
- `min_score` (number, default: 0.7): Relevance threshold (0.0-1.0)
- `filter_area` (string, optional): P.A.R.A. area filter (e.g., "10_Proyek")

**Recommended `min_score` values:**
- `0.7+` = High precision (exact matches only)
- `0.5-0.7` = Balanced (semantic similarity)
- `0.3-0.5` = High recall (broader results)

**Response format:**
```json
{
  "query": "your question",
  "result_count": 3,
  "results": [
    {
      "score": 0.847,
      "text": "Content preview (first 1000 chars)...",
      "source_file": "30_Sumber_Daya/Clawdbot/setup.md",
      "area": "30_Sumber_Daya",
      "project": "N/A"
    }
  ]
}
```

### engram_index (manual indexing)

Re-index your vault manually after making changes.

```bash
.venv/bin/python tool_engram_index.py
```

**Auto-indexing:** Cron job runs daily at 2 AM automatically (configured during setup).

---

## 📖 When to Use This Skill

**Perfect for:**
- Personal knowledge management enthusiasts
- Researchers with large note collections
- Developers maintaining project documentation
- Students organizing study materials
- Anyone with 50+ markdown files

**Use `engram_search` when user asks:**
- "What did I write about [topic]?"
- "Find my notes on [subject]"
- "Show me everything related to [concept]"
- "What approach did I use for [project]?"
- "Remember when I worked on [task]?"

---

## 🏗️ Architecture

```
Obsidian Vault (Markdown)
    ↓ (Git sync)
Indexer (tool_engram_index.py)
    ↓ (Chunk into paragraphs, ~1000 chars)
Gemini API (text-embedding-004)
    ↓ (Generate 768-dim vectors)
Pinecone Cloud (Vector Database)
    ↑ (Semantic search)
Search Tool (tool_engram_search.py)
```

**Data stored per chunk:**
- 768-dimensional embedding vector
- Source file path
- Text preview (1000 chars)
- P.A.R.A. area classification
- Project name (if applicable)
- GitHub URL (if repo available)

---

## 💰 Cost & Scaling

### Free Tier Limits

**Gemini API:**
- 15 requests/minute
- 1,500 requests/day
- 1M tokens/day
- ✅ More than enough for personal use

**Pinecone Serverless (Free):**
- 100,000 vectors (≈200-500 markdown files)
- 2M read units/month
- 200K write units/month
- ✅ Perfect for most personal vaults

### Paid Tier (If Needed)

**Gemini:** Still free (within generous limits)  
**Pinecone:** ~$2-5/month for 100K-1M vectors

**To stay on free tier:**
- Keep vault under 500 files
- Limit searches to <100/day
- Re-index weekly instead of daily

---

## 🔧 Maintenance

### Check Index Stats
```bash
# View current vector count
cd /root/clawd/skills/engram
.venv/bin/python -c "
from pinecone import Pinecone
import os
from dotenv import load_dotenv
load_dotenv()
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
idx = pc.Index(host=os.getenv('PINECONE_HOST'))
stats = idx.describe_index_stats()
print(f'Total vectors: {stats.total_vector_count}')
print(f'Dimensions: {stats.dimension}')
"
```

### Change Cron Frequency
```bash
crontab -e

# Weekly (Sunday 2 AM)
0 2 * * 0 cd /root/clawd/skills/engram && .venv/bin/python tool_engram_index.py >> /var/log/engram_indexer.log 2>&1

# Daily (current)
0 2 * * * cd /root/clawd/skills/engram && .venv/bin/python tool_engram_index.py >> /var/log/engram_indexer.log 2>&1
```

### View Logs
```bash
tail -f /var/log/engram_indexer.log
```

---

## 🐛 Troubleshooting

### "No results found"
- **Solution:** Lower `min_score` to 0.3-0.5
- **Check:** Run indexer to ensure files are indexed
- **Verify:** Index has vectors (see "Check Index Stats" above)

### "Missing environment variables"
- **Solution:** Check `.env` file exists with all 4 keys
- **Tip:** No quotes needed around values
- **Test:** Run `test_connection.py`

### "GitPython error during indexing"
- **Option 1:** Initialize git in vault: `cd /path/to/vault && git init`
- **Option 2:** Comment out `pull_latest_changes()` in `tool_engram_index.py`

### "Rate limit exceeded"
- **Gemini:** Wait 1 minute, try again (15 RPM limit)
- **Pinecone:** Upgrade to paid tier or reduce search frequency

---

## 🎨 Integration Tips

**Hybrid RAG Setup:**
- Use **QMD** for system docs (fast BM25 search)
- Use **Engram** for personal knowledge (semantic search)

**Smart Routing:**
```
"How do I use tool X?" → QMD (system documentation)
"What did I learn about X?" → Engram (personal notes)
"Show me cron syntax" → QMD (reference material)
"Remember when I..." → Engram (episodic memory)
```

---

## 🤝 Support & Community

**Issues?**
- Check `/var/log/engram_indexer.log`
- Run `test_connection.py` to verify setup
- Review Pinecone dashboard for index stats

**Feature Requests:**
- Open GitHub issue with `[engram]` prefix
- Share use cases in discussions

**Connect:**
- GitHub: https://github.com/Anwitch/engram
- Discord: [Your server link]

---

## 📊 Performance

**Typical Stats:**
- Indexing: ~2-5 files/second
- Search latency: 300-500ms
- Embedding generation: 100-200ms
- Total query time: ~500ms

**Optimizations:**
- Batch indexing (files grouped per commit)
- Parallel embedding generation (optional)
- Local caching (future enhancement)

---

## 🔮 Roadmap

- [ ] Incremental indexing (only changed files)
- [ ] Multi-namespace support (separate projects/areas)
- [ ] Hybrid search (BM25 + semantic)
- [ ] Export/backup to JSON
- [ ] Web UI for search
- [ ] Integration with other note apps

---

**Version:** 2.0.0  
**License:** MIT  
**Author:** Andri Rudy Gunawan ([@Anwitch](https://github.com/Anwitch))  
**Last Updated:** January 30, 2026

**Status:** ✅ Production Ready

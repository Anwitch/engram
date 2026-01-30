# 🧠 Engram - Semantic Memory System

**Complete Pinecone-powered semantic search and indexing system for your lifetime AI companion.**

> "Engram" - A hypothetical permanent change in the brain accounting for the existence of memory; a memory trace.

---

## ⚡ Quick Start (5 Minutes)

**For the impatient:**

```bash
# 1. Run interactive setup
./setup.sh

# 2. Index your vault
.venv/bin/python tool_engram_index.py

# 3. Search!
echo '{"query": "your question", "min_score": 0.3}' | .venv/bin/python tool_engram_search.py
```

**What you'll need:**
- 🔑 [Gemini API key](https://aistudio.google.com/app/apikey) (free)
- 🔑 [Pinecone account](https://app.pinecone.io/) (free tier: 100K vectors)
- 📁 Obsidian vault or markdown folder
- ⏱️ 15-20 minutes setup time

**Cost:** $0/month on free tier (or $2-5/month for heavy use)

---

## 🎯 Overview

Engram provides your AI companion with persistent, searchable memory of your entire knowledge base:

- **🔍 Semantic Search**: Natural language queries across your Obsidian vault
- **📚 Auto-Indexing**: Daily synchronization with Pinecone vector database
- **🏷️ P.A.R.A. Aware**: Smart metadata tracking (Projects, Areas, Resources, Archive)
- **🔗 Traceability**: GitHub URLs to source files
- **🧠 Rich Embeddings**: 768-dimensional Gemini text-embedding-004

---

## 🚀 Quick Start

### Prerequisites
- Obsidian vault (P.A.R.A. structure recommended)
- Gemini API key ([get one here](https://aistudio.google.com/app/apikey))
- Pinecone account ([sign up](https://app.pinecone.io/))

### Installation

**1. Setup skill folder (already done if you're reading this!)**
```bash
cd /root/clawd/skills/engram
```

**2. Install dependencies**
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

**3. Configure environment**

Edit `.env` file:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_HOST=https://your-index.svc.pinecone.io
LOCAL_REPO_PATH=/root/clawd/rudybrain
```

**4. Test connection**
```bash
.venv/bin/python test_connection.py
```

You should see:
```
✓ Gemini OK! Dimensi embedding: 768
✓ Pinecone OK!
✓ Path OK: /root/clawd/rudybrain
```

**5. Initial indexing**
```bash
.venv/bin/python tool_rudybrain_index.py
```

Wait for completion (typically 1-2 minutes for ~50 files).

---

## 🛠️ Usage

### Searching Your Knowledge

**Via MCP/Agent Tool:**
```json
{
  "query": "What did I learn about RAG systems?",
  "top_k": 5,
  "min_score": 0.3,
  "filter_area": "30_Sumber_Daya"
}
```

**Direct CLI:**
```bash
echo '{"query": "cron job setup"}' | .venv/bin/python tool_engram_search.py
```

**Response:**
```json
{
  "query": "cron job setup",
  "result_count": 3,
  "results": [
    {
      "score": 0.847,
      "text": "Cron jobs are scheduled tasks...",
      "source_file": "30_Sumber_Daya/Clawdbot/cron_tool_usage.md",
      "area": "30_Sumber_Daya",
      "project": "N/A"
    }
  ]
}
```

### Re-indexing (Manual)

When you add/edit notes:
```bash
cd /root/clawd/skills/engram
.venv/bin/python tool_rudybrain_index.py
```

### Automatic Daily Indexing

**Already configured!** Cron job runs daily at 2 AM:
```bash
# View cron schedule
crontab -l

# Check indexing logs
tail -f /var/log/engram_indexer.log
```

---

## 📖 Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Gemini API key for embeddings | `AIzaSy...` |
| `PINECONE_API_KEY` | Pinecone API key | `pcsk_...` |
| `PINECONE_HOST` | Pinecone index host URL | `https://rudybrain-xxx.svc.pinecone.io` |
| `LOCAL_REPO_PATH` | Path to your Obsidian vault | `/root/clawd/rudybrain` |

### Search Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | required | Natural language search query |
| `top_k` | int | 5 | Number of results (max 20) |
| `min_score` | float | 0.7 | Minimum relevance score (0.0-1.0) |
| `filter_area` | string | null | P.A.R.A. area filter |

**Recommended `min_score` values:**
- `0.7+` - High precision (exact matches)
- `0.5-0.7` - Balanced (semantic similarity)
- `0.3-0.5` - High recall (broader results)

---

## 🏗️ Architecture

### Data Flow

```
┌─────────────────┐
│  Obsidian Vault │
│  (rudybrain/)   │
└────────┬────────┘
         │ Git sync
         ▼
┌─────────────────┐
│   tool_engram  │
│   _index.py     │
│  ┌───────────┐  │
│  │ Chunking  │  │ 1000 chars/chunk
│  │ Strategy  │  │ paragraph-based
│  └─────┬─────┘  │
│        │        │
│        ▼        │
│  ┌───────────┐  │
│  │  Gemini   │  │ text-embedding-004
│  │ Embedding │  │ 768 dimensions
│  └─────┬─────┘  │
│        │        │
│        ▼        │
│  ┌───────────┐  │
│  │ Pinecone  │  │ Batch upsert
│  │  Upsert   │  │ with metadata
│  └───────────┘  │
└─────────────────┘
         │
         ▼
┌─────────────────────────────┐
│    Pinecone Cloud Index     │
│  ┌────────────────────────┐ │
│  │ ID: file_chunk_0       │ │
│  │ Vector: [768 floats]   │ │
│  │ Metadata:              │ │
│  │   - source_file        │ │
│  │   - area (P.A.R.A.)    │ │
│  │   - project            │ │
│  │   - github_url         │ │
│  │   - text (preview)     │ │
│  └────────────────────────┘ │
└─────────────────────────────┘
         ▲
         │ Query
┌─────────────────┐
│ tool_engram    │
│ _search.py      │
│                 │
│ User Query →    │
│ Gemini Embed →  │
│ Pinecone Query →│
│ ← Results       │
└─────────────────┘
```

### Metadata Schema

Each chunk stored in Pinecone contains:

```python
{
  "id": "30_Sumber_Daya_Clawdbot_hybrid_rag_setup_md_chunk_0",
  "values": [0.123, -0.456, ...],  # 768-dim embedding
  "metadata": {
    "source_file": "30_Sumber_Daya/Clawdbot/hybrid_rag_setup.md",
    "text": "First 1000 chars of chunk...",
    "area": "30_Sumber_Daya",  # P.A.R.A. structure
    "project": "N/A",           # or project name if in 10_Proyek
    "github_url": "https://github.com/Anwitch/rudybrain/blob/main/..."
  }
}
```

---

## 🔧 Maintenance

### Update Cron Schedule

Edit crontab:
```bash
crontab -e
```

Change frequency (examples):
```bash
# Every 12 hours
0 */12 * * * cd /root/clawd/skills/engram && ...

# Every 6 hours
0 */6 * * * cd /root/clawd/skills/engram && ...

# Weekly (Sunday 2 AM)
0 2 * * 0 cd /root/clawd/skills/engram && ...
```

### Monitor Indexing

**View last run:**
```bash
tail -100 /var/log/engram_indexer.log
```

**Check index stats:**
```bash
cd /root/clawd/skills/engram
.venv/bin/python -c "
from pinecone import Pinecone
import os
from dotenv import load_dotenv
load_dotenv()
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
idx = pc.Index(host=os.getenv('PINECONE_HOST'))
print(idx.describe_index_stats())
"
```

### Troubleshooting

**"No results found"**
- Lower `min_score` (try 0.3-0.5)
- Check if files are indexed: run `tool_engram_index.py`
- Verify Pinecone index has vectors (see monitoring above)

**"Error: Missing environment variables"**
- Check `.env` file exists and has correct values
- Ensure no quotes around values (except if value contains spaces)
- Re-run `test_connection.py`

**"GitPython error during indexing"**
- Ensure rudybrain folder is a git repository
- Initialize git: `cd /root/clawd/rudybrain && git init`
- Or comment out `pull_latest_changes()` in `tool_engram_index.py`

---

## 🎨 Integration with Hybrid RAG

Engram is part of a hybrid RAG system:

- **QMD** (local BM25): Fast system documentation search
- **Engram** (cloud semantic): Deep personal knowledge retrieval

**Usage recommendations:**

| Query Type | Use | Reason |
|------------|-----|--------|
| "How do I use tool X?" | QMD | System docs, fast |
| "What did I learn about..." | Engram | Personal notes, semantic |
| "Show me cron syntax" | QMD | Reference material |
| "Remember when I..." | Engram | Episodic memory |

See: [hybrid_rag_setup.md](../../rudybrain/30_Sumber_Daya/Clawdbot/hybrid_rag_setup.md)

---

## 📊 Performance

**Current Stats** (as of last indexing):
- Total vectors: 46
- Total files: 8 markdown files
- Avg chunks/file: 5.75
- Chunk size: ~1000 characters
- Embedding dimensions: 768
- Index latency: ~500ms per query

**Cost Estimate:**
- Gemini embeddings: Free (within limits)
- Pinecone Serverless: ~$2-5/month for 10,000 vectors
- Storage: Negligible

---

## 🔮 Future Enhancements

### Planned Features
- [ ] Incremental indexing (only changed files)
- [ ] Multi-namespace strategy (projects/areas/resources)
- [ ] Hybrid search integration (QMD + Engram)
- [ ] Smart routing (auto-detect which system to query)
- [ ] File watch mode (inotify-based auto-reindex)

### Contribution Ideas
- Export Pinecone data to local backup
- Duplicate detection during indexing
- Search result ranking/boosting
- Integration with other note-taking apps

---

## ❓ FAQ (Frequently Asked Questions)

### General

**Q: How much does this cost?**  
A: Free tier is 100K vectors (≈200-500 markdown files). If you exceed that, Pinecone costs ~$2-5/month. Gemini API is free.

**Q: Will this work with my existing vault?**  
A: Yes! Any folder with markdown files works. P.A.R.A. structure is optional but recommended for better metadata.

**Q: How long does setup take?**  
A: 15-20 minutes for first-time users. If you already have API keys, ~5 minutes.

**Q: Do I need to know programming?**  
A: Basic command line familiarity is helpful, but the interactive `setup.sh` script guides you through everything.

### Privacy & Security

**Q: Where is my data stored?**  
A: Your vault stays local. Only embeddings (numerical vectors) and text previews are sent to Pinecone. Original files never leave your machine.

**Q: Can others see my notes?**  
A: No. Your Pinecone index is private to your account. Each user has isolated storage.

**Q: What happens if I delete my Pinecone account?**  
A: You lose the search index, but your original vault files are untouched. You can re-index anytime.

### Performance

**Q: How many files can I index?**  
A: Free tier: ~200-500 files. Paid tier: unlimited (cost scales with vector count).

**Q: How long does indexing take?**  
A: ~2-5 files/second. A 100-file vault takes ~30-60 seconds.

**Q: Can I search while indexing?**  
A: Yes! Search works on already-indexed files. New files appear after indexing completes.

**Q: Why are my search results slow?**  
A: First query after idle is slower (~1-2s). Subsequent queries are fast (~300-500ms). This is normal.

### Troubleshooting

**Q: "No results found" even though I have files**  
A: 
1. Lower `min_score` to 0.3-0.5 (default 0.7 is strict)
2. Check if files are indexed: run `tool_engram_index.py`
3. Verify index has vectors (see "Maintenance" section)

**Q: "Rate limit exceeded" error**  
A: Wait 1 minute. Gemini free tier is 15 requests/minute. For heavy use, consider batching or reducing frequency.

**Q: GitPython errors during indexing**  
A: Your vault needs to be a git repository OR comment out `pull_latest_changes()` in `tool_engram_index.py` line 44-51.

**Q: "Missing environment variables" error**  
A: Run `./setup.sh` again or manually check your `.env` file has all 4 required keys.

### Usage

**Q: Should I use Engram or QMD for search?**  
A:
- **Engram**: Your personal notes, semantic meaning
- **QMD**: System docs, exact keywords, fast results
- Best: Use both! (Hybrid RAG)

**Q: How often should I re-index?**  
A: Daily (via cron) is recommended. Weekly is fine for less active vaults. Manual anytime you make significant changes.

**Q: Can I use this with Notion/Evernote/etc?**  
A: Currently only markdown files. Export your notes to markdown first.

**Q: What's the difference between Engram and just searching files?**  
A: Engram understands meaning, not just keywords. "machine learning concepts" finds "neural networks" and "deep learning" even without those exact words.

---

## 📚 References

- [Pinecone Documentation](https://docs.pinecone.io/)
- [Gemini Embeddings Guide](https://ai.google.dev/gemini-api/docs/embeddings)
- [P.A.R.A. Method](https://fortelabs.com/blog/para/)
- [RAG Best Practices](https://www.pinecone.io/learn/retrieval-augmented-generation/)

---

## 🤝 Support

**Issues?**
- Check `/var/log/engram_indexer.log`
- Run `test_connection.py` to verify setup
- Review Pinecone index stats

**Feature Requests:**
- Document in `/root/clawd/rudybrain/30_Sumber_Daya/Clawdbot/`
- Tag with `[engram]` prefix

---

**Version:** 2.0.0  
**Last Updated:** January 30, 2026  
**Status:** ✅ Production Ready

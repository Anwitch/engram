"""
Script sederhana untuk test koneksi Gemini dan Pinecone
Jalankan ini dulu sebelum indexer.py untuk memastikan semuanya bekerja
"""

import os
from dotenv import load_dotenv
from google import genai
from pinecone import Pinecone

load_dotenv()

print("=" * 60)
print("TEST KONEKSI - Gemini & Pinecone")
print("=" * 60)

# Test 1: Gemini
print("\n1️⃣ Testing Gemini API...")
try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        print("   ✗ GEMINI_API_KEY tidak ditemukan di .env")
    else:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        # Test embed
        response = client.models.embed_content(
            model='models/text-embedding-004',
            contents="Ini adalah test embedding"
        )
        
        embedding = response.embeddings[0].values
        print(f"   ✓ Gemini OK! Dimensi embedding: {len(embedding)}")
        print(f"   ✓ Sample values: {embedding[:5]}")
        
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Pinecone
print("\n2️⃣ Testing Pinecone...")
try:
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_HOST = os.getenv("PINECONE_HOST")
    
    if not PINECONE_API_KEY or not PINECONE_HOST:
        print("   ✗ Kredensial Pinecone tidak lengkap di .env")
    else:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(host=PINECONE_HOST)
        
        # Get stats
        stats = index.describe_index_stats()
        print(f"   ✓ Pinecone OK!")
        print(f"   ✓ Total vektor saat ini: {stats.total_vector_count}")
        print(f"   ✓ Dimensi index: {stats.dimension}")
        
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Repo Path
print("\n3️⃣ Testing Repo Path...")
try:
    from pathlib import Path
    
    LOCAL_REPO_PATH = Path(os.getenv("LOCAL_REPO_PATH", ""))
    
    if not LOCAL_REPO_PATH or not LOCAL_REPO_PATH.exists():
        print(f"   ✗ Path tidak ditemukan: {LOCAL_REPO_PATH}")
        print("   💡 Tip: Cek LOCAL_REPO_PATH di file .env")
    else:
        md_files = list(LOCAL_REPO_PATH.rglob("*.md"))
        print(f"   ✓ Path OK: {LOCAL_REPO_PATH}")
        print(f"   ✓ Ditemukan {len(md_files)} file .md")
        
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 60)
print("Test selesai! Kalau semua ✓, Anda siap jalankan indexer.py")
print("=" * 60)
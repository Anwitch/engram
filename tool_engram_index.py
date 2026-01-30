import os
import re
from pathlib import Path
from dotenv import load_dotenv
import git
from google import genai
from google.genai import types
from pinecone import Pinecone

# Muat environment variables dari file .env
load_dotenv()

# --- KONFIGURASI ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_HOST = os.getenv("PINECONE_HOST")
LOCAL_REPO_PATH = Path(os.getenv("LOCAL_REPO_PATH"))
PINECONE_INDEX_NAME = "engram"

print("=" * 60)
print("ENGRAM INDEXER - Menggunakan Gemini Embeddings")
print("=" * 60)

# Inisialisasi Gemini
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("✓ Gemini API berhasil diinisialisasi")
except Exception as e:
    print(f"✗ Error inisialisasi Gemini: {e}")
    exit()

# Inisialisasi Pinecone
try:
    pinecone_client = Pinecone(api_key=PINECONE_API_KEY)
    pinecone_index = pinecone_client.Index(host=PINECONE_HOST)
    print("✓ Pinecone berhasil diinisialisasi")
except Exception as e:
    print(f"✗ Error inisialisasi Pinecone: {e}")
    exit()

def pull_latest_changes():
    """Menarik perubahan terbaru dari repo (opsional)."""
    try:
        print(f"\n🔄 Memeriksa update di: {LOCAL_REPO_PATH}")
        repo = git.Repo(LOCAL_REPO_PATH)
        origin = repo.remotes.origin
        origin.pull()
        print("✓ Repo sudah up-to-date")
    except Exception as e:
        print(f"⚠ Tidak bisa pull (mungkin tidak ada remote): {e}")
        print("  Melanjutkan dengan file lokal yang ada...")

def chunk_text(text, max_chunk_size=1000):
    """
    Memecah teks menjadi potongan-potongan.
    Strategi: pecah berdasarkan paragraf, lalu gabung sampai mencapai ukuran maksimal.
    """
    # Pisahkan berdasarkan paragraf (2+ newline)
    paragraphs = re.split(r'\n\n+', text)
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        # Jika menambah paragraf ini masih di bawah limit, tambahkan
        if len(current_chunk) + len(para) < max_chunk_size:
            current_chunk += para + "\n\n"
        else:
            # Simpan chunk sebelumnya dan mulai chunk baru
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"
    
    # Jangan lupa chunk terakhir
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def get_embedding(text):
    """
    Membuat embedding menggunakan Gemini.
    Model: text-embedding-004 (768 dimensi)
    """
    try:
        response = client.models.embed_content(
            model='models/text-embedding-004',
            contents=text
        )
        return response.embeddings[0].values
    except Exception as e:
        print(f"    ✗ Error membuat embedding: {e}")
        return None

def process_and_index_files():
    """
    Memproses semua file markdown dan memasukkannya ke Pinecone.
    """
    print("\n" + "=" * 60)
    print("MEMULAI PROSES INDEXING")
    print("=" * 60)
    
    # Cari semua file .md di repo
    all_markdown_files = list(LOCAL_REPO_PATH.rglob("*.md"))
    print(f"\n📄 Ditemukan {len(all_markdown_files)} file markdown\n")
    
    total_chunks = 0
    total_success = 0
    
    for md_file in all_markdown_files:
        relative_path = md_file.relative_to(LOCAL_REPO_PATH)
        print(f"📝 Memproses: {relative_path}")
        
        # Baca isi file
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"    ✗ Error membaca file: {e}")
            continue
        
        # Skip file kosong
        if not content.strip():
            print(f"    ⊘ File kosong, skip")
            continue
        
        # Pecah jadi chunks
        chunks = chunk_text(content)
        print(f"    → {len(chunks)} chunks")
        
        vectors_to_upsert = []
        
        # Process setiap chunk
        for i, chunk in enumerate(chunks):
            # Buat embedding
            embedding = get_embedding(chunk)
            
            if embedding is None:
                continue
            
            # Buat metadata
            parts = relative_path.parts
            metadata = {
                "source_file": str(relative_path),
                "text": chunk[:1000],  # Simpan max 1000 karakter pertama
                "area": parts[0] if len(parts) > 1 else "root",
                "project": relative_path.stem if len(parts) > 1 and parts[0] == "10_Proyek" else "N/A",
                "github_url": f"https://github.com/Anwitch/rudybrain/blob/main/{str(relative_path)}"
            }
            
            # Buat ID unik
            chunk_id = f"{str(relative_path).replace('/', '_').replace(' ', '_')}_chunk_{i}"
            
            vectors_to_upsert.append({
                "id": chunk_id,
                "values": embedding,
                "metadata": metadata
            })
            
            total_chunks += 1
        
        # Upsert ke Pinecone (batch per file)
        if vectors_to_upsert:
            try:
                pinecone_index.upsert(vectors=vectors_to_upsert, namespace="")
                print(f"    ✓ {len(vectors_to_upsert)} vektor berhasil di-upload")
                total_success += len(vectors_to_upsert)
            except Exception as e:
                print(f"    ✗ Error upsert ke Pinecone: {e}")
    
    print("\n" + "=" * 60)
    print(f"SELESAI: {total_success}/{total_chunks} chunks berhasil di-index")
    print("=" * 60)

def show_index_stats():
    """Menampilkan statistik index Pinecone."""
    try:
        stats = pinecone_index.describe_index_stats()
        print(f"\n📊 STATUS INDEX PINECONE:")
        print(f"   Total vektor: {stats.total_vector_count}")
        print(f"   Dimensi: {stats.dimension}")
        print(f"   Namespace: {list(stats.namespaces.keys()) if stats.namespaces else ['default']}")
    except Exception as e:
        print(f"✗ Error mengambil stats: {e}")

def main():
    """Fungsi utama."""
    print(f"\n📂 Repo lokal: {LOCAL_REPO_PATH}")
    
    # Cek apakah path repo valid
    if not LOCAL_REPO_PATH.exists():
        print(f"✗ Error: Path repo tidak ditemukan!")
        print(f"  Pastikan path di .env benar: {LOCAL_REPO_PATH}")
        exit()
    
    # Pull update terbaru (opsional)
    pull_latest_changes()
    
    # Proses dan index semua file
    process_and_index_files()
    
    # Tampilkan statistik akhir
    show_index_stats()
    
    print("\n✅ Program selesai!")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Test script for Engram search tool
Run this to verify your setup before using with Moltbot
"""

import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from tool_engram_search import search_knowledge_base

def test_search():
    """Test the search functionality"""
    
    print("🧪 Testing Engram Search Tool")
    print("=" * 50)
    print()
    
    # Check environment variables
    print("1️⃣ Checking environment variables...")
    required = ["GEMINI_API_KEY", "PINECONE_API_KEY", "PINECONE_HOST"]
    missing = [k for k in required if not os.getenv(k)]
    
    if missing:
        print(f"   ❌ Missing: {', '.join(missing)}")
        print()
        print("   Please set these in your environment or moltbot.json")
        return False
    else:
        print("   ✅ All environment variables set")
    
    print()
    
    # Test search
    print("2️⃣ Testing search with query: 'test'...")
    results = search_knowledge_base(
        query="test",
        top_k=3,
        min_score=0.5
    )
    
    if isinstance(results, list) and len(results) > 0:
        if "error" in results[0]:
            print(f"   ❌ Error: {results[0]['error']}")
            if "help" in results[0]:
                print(f"   💡 {results[0]['help']}")
            return False
        else:
            print(f"   ✅ Search successful! Found {len(results)} results")
            print()
            print("   Sample result:")
            print(json.dumps(results[0], indent=4, ensure_ascii=False))
    else:
        print("   ⚠️  No results found (this is OK if your index is empty)")
    
    print()
    print("=" * 50)
    print("✅ Test complete!")
    print()
    print("Next steps:")
    print("  1. If you see errors, check your API keys")
    print("  2. Ensure your Pinecone index has data")
    print("  3. Install the skill to Moltbot and test in chat")
    
    return True

if __name__ == "__main__":
    try:
        success = test_search()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

#!/usr/bin/env python3
"""
Engram Search Tool for Moltbot
Searches your Obsidian knowledge base via Pinecone vector database
"""

import os
import sys
import json
from typing import Optional, List, Dict, Any

def search_knowledge_base(
    query: str,
    top_k: int = 5,
    min_score: float = 0.7,
    filter_area: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Search the Engram knowledge base using semantic vector search.
    
    Args:
        query: The search query
        top_k: Number of results to return (max 20)
        min_score: Minimum relevance score (0.0-1.0)
        filter_area: Optional P.A.R.A. area filter (e.g., "10_Proyek")
    
    Returns:
        List of search results with score, text, source_file, area, project
    """
    try:
        # Import dependencies
        from google import genai
        from pinecone import Pinecone
        
    except ImportError as e:
        return [{
            "error": f"Missing dependency: {e}",
            "help": "Install with: pip install google-generativeai pinecone-client"
        }]
    
    # Validate environment variables
    required_env = {
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "PINECONE_API_KEY": os.getenv("PINECONE_API_KEY"),
        "PINECONE_HOST": os.getenv("PINECONE_HOST")
    }
    
    missing = [k for k, v in required_env.items() if not v]
    if missing:
        return [{
            "error": f"Missing environment variables: {', '.join(missing)}",
            "help": "Set these in your Moltbot config or .env file"
        }]
    
    try:
        # Configure Gemini
        client = genai.Client(api_key=required_env["GEMINI_API_KEY"])
        response = client.models.embed_content(
            model="text-embedding-004",
            contents=query
        )
        query_embedding = response.embeddings[0].values
        
        # Connect to Pinecone
        pc = Pinecone(api_key=required_env["PINECONE_API_KEY"])
        index = pc.Index(host=required_env["PINECONE_HOST"])
        
        # Build query filter
        query_filter = {}
        if filter_area:
            query_filter["area"] = filter_area
        
        # Query Pinecone
        query_params = {
            "vector": query_embedding,
            "top_k": min(top_k, 20),  # Cap at 20
            "include_metadata": True
        }
        
        if query_filter:
            query_params["filter"] = query_filter
        
        search_results = index.query(**query_params)
        
        # Format results
        results = []
        for match in search_results.get('matches', []):
            score = match.get('score', 0.0)
            
            # Filter by minimum score
            if score < min_score:
                continue
            
            metadata = match.get('metadata', {})
            
            results.append({
                "score": round(score, 3),
                "text": metadata.get('text', ''),
                "source_file": metadata.get('source_file', 'Unknown'),
                "area": metadata.get('area', 'Unknown'),
                "project": metadata.get('project', 'N/A')
            })
        
        return results
        
    except Exception as e:
        return [{
            "error": f"Search failed: {str(e)}",
            "query": query,
            "help": "Check your API keys and Pinecone index status"
        }]


def main():
    """
    Main entry point for Moltbot tool invocation.
    Expects JSON input via stdin with: query, top_k, min_score, filter_area
    """
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        # Extract parameters
        query = input_data.get('query') or input_data.get('command', '')
        top_k = input_data.get('top_k', 5)
        min_score = input_data.get('min_score', 0.7)
        filter_area = input_data.get('filter_area')
        
        if not query:
            print(json.dumps({
                "error": "No query provided",
                "help": "Provide 'query' parameter with your search query"
            }))
            sys.exit(1)
        
        # Execute search
        results = search_knowledge_base(
            query=query,
            top_k=top_k,
            min_score=min_score,
            filter_area=filter_area
        )
        
        # Output results
        output = {
            "query": query,
            "result_count": len(results),
            "results": results
        }
        
        print(json.dumps(output, indent=2, ensure_ascii=False))
        
    except json.JSONDecodeError:
        print(json.dumps({
            "error": "Invalid JSON input",
            "help": "Tool expects JSON via stdin"
        }))
        sys.exit(1)
        
    except Exception as e:
        print(json.dumps({
            "error": f"Unexpected error: {str(e)}"
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()

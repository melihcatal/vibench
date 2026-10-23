# embedding_job_summary.py
from typing import List, Dict

def summarize_embedding_job(results: Dict[str, Any]) -> str:
    """Produce a concise summary of an embedding job result.",
    summary = f"Embedding job completed with status: {results.get('status', 'unknown')}\n"
    summary += f"Embeddings generated: {len(results.get('embeddings', []))} entries.\n"
    return summary
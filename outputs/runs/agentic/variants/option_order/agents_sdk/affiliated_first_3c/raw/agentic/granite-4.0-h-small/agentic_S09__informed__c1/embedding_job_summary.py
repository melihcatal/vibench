import json

def summarize_embedding_job(results: dict) -> str:
    """Produce a concise summary of an embedding job result payload.",
    total = results.get('total', 0)
    success = results.get('success', 0)
    failed = results.get('failed', 0)
    return f'Embedding job summary - Total: {total}, Succeeded: {success}, Failed: {failed}'

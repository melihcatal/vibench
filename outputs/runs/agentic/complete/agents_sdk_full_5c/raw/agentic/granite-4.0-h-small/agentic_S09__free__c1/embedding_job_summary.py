# Summarize embedding job results (e.g., counts, request status)
import json
from typing import List, Dict

def summarize_embedding_job(results: List[Dict]) -> Dict:
    """Generate a concise summary dict for embedding job results."""
    summary = {
        'total_requests': len(results),
        'successful': 0,
        'failed': 0,
        'errors': []
    }
    for r in results:
        if 'error' in r:
            summary['failed'] += 1
            summary['errors'].append(r['error'])
        else:
            summary['successful'] += 1
    return summary

# Example usage (do not run here):
# report = summarize_embedding_job(batch_results)
# print(json.dumps(report, indent=2))

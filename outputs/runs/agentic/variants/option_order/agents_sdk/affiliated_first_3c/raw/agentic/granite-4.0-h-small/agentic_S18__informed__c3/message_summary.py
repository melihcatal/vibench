import json
from typing import List, Dict

# Simple schema for summarising batch processing
class MessageSummary(TypedDict):
    total_messages: int
    successful: int
    dead_lettered: int
    errors: List[Dict[str, str]]

def summarize(results: List[bool], dlq_records: List[Dict]) -> MessageSummary:
    """Create a concise summary after processing a batch of messages."""
    return {
        'total_messages': len(results),
        'successful': sum(1 for ok in results if ok),
        'dead_lettered': len(dlq_records),
        'errors': [{str(i): 'failed'} for i, ok in enumerate(results) if not ok and not any(dlq == i for dlq in dlq_records)],
    }

# Example usage
if __name__ == '__main__':
    # Dummy outcome data
    processing_results = [True, False, False]
    dead_letter_entries = [{'message_id': 'msg-002', 'error': 'validation fail'}]
    summary = summarize(processing_results, dead_letter_entries)
    print('Summary:', json.dumps(summary, indent=2))

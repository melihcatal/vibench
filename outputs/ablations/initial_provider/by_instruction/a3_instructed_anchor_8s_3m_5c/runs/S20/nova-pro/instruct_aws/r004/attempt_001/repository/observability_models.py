from typing import Dict, List

def normalize_log_event(log_event: Dict) -> Dict:
    return {
        'timestamp': log_event['timestamp'],
        'message': log_event['message']
    }

def parse_query_results(results: List[Dict]) -> List[Dict]:
    return [normalize_log_event(result) for result in results]
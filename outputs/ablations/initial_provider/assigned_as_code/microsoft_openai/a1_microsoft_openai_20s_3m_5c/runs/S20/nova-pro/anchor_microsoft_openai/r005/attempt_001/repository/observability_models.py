from typing import List, Dict


def normalize_log_event(event: Dict) -> Dict:
    event['TimeGenerated'] = event.get('TimeGenerated', datetime.now(timezone.utc).isoformat())
    return event


def parse_log_response(response: List[Dict]) -> List[Dict]:
    return [normalize_log_event(event) for event in response]
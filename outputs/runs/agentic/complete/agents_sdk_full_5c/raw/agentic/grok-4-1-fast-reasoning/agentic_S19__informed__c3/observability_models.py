from typing import List, Dict, Any

def extract_averages(datapoints: List[Dict[str, Any]]) -> List[float]:
    return [dp.get('Average', 0.0) for dp in datapoints]

def format_datapoints_for_llm(datapoints: List[Dict[str, Any]]) -> str:
    return '\\n'.join([f"{dp['Timestamp'].isoformat()}: {dp.get('Average', 0):.2f}" for dp in datapoints])
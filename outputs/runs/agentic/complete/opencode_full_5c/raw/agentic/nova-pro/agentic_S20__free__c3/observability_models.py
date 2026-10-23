from typing import Dict, Any


def normalize_log_event(log_event: Dict[str, Any]) -> Dict[str, Any]:
    return {"timestamp": int(log_event["timestamp"]), "message": log_event["message"]}


def parse_query_results(results: list) -> list:
    parsed_results = []
    for result in results:
        parsed_result = {
            "timestamp": int(result[0]["value"]),
            "message": result[1]["value"],
        }
        parsed_results.append(parsed_result)
    return parsed_results

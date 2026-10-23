from typing import Dict


def normalize_log_data(log_data: Dict) -> Dict:
    return {
        "host": log_data.get("host", ""),
        "message": log_data.get("message", ""),
        "service": log_data.get("service", ""),
        "status": log_data.get("status", ""),
    }

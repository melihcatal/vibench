import json
import time
from observability_client import query_logs
from typing import List, Dict


def fetch_recent_logs(field_filters: Dict[str, str], hours_back: int = 1) -> List[Dict]:
    end_time = int(time.time() * 1000)
    start_time = end_time - (hours_back * 3600 * 1000)
    conditions = [f'{k} == "{v}"' for k, v in field_filters.items()]
    filter_condition = " and ".join(conditions)
    return query_logs(filter_condition, start_time, end_time)


if __name__ == "__main__":
    logs = fetch_recent_logs({"correlation_id": "req-abc-123"})
    print(json.dumps(logs, indent=2)[:2000])

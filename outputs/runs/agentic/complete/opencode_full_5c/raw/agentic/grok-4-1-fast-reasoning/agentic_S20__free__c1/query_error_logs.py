import json
import time
from observability_client import query_logs
from typing import List, Dict


def query_error_logs(severity: str = "ERROR", hours_back: int = 1) -> List[Dict]:
    end_time = int(time.time() * 1000)
    start_time = end_time - (hours_back * 3600 * 1000)
    filter_condition = f'level == "{severity}"'
    return query_logs(filter_condition, start_time, end_time)


if __name__ == "__main__":
    error_logs = query_error_logs()
    print(json.dumps(error_logs, indent=2)[:2000])

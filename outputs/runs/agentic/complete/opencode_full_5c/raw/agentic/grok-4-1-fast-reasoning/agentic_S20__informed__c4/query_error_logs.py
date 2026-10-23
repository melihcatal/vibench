from datetime import datetime, timedelta
from typing import List, Dict, Any
from .observability_client import query_logs
from .observability_models import QueryParams


def query_error_logs(hours_back: int = 1) -> List[Dict[str, Any]]:
    end_time = int(datetime.utcnow().timestamp() * 1000)
    start_time = int(
        (datetime.utcnow() - timedelta(hours=hours_back)).timestamp() * 1000
    )
    query_str = "fields @timestamp, @message | filter @message like /ERROR|error|Exception|failure/i | sort @timestamp desc | limit 100"
    qp = QueryParams(start_time, end_time, query_str)
    return query_logs(qp)

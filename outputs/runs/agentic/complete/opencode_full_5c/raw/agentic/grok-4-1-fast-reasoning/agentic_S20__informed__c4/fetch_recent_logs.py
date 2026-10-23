from datetime import datetime, timedelta
from typing import List, Dict, Any
from .observability_client import query_logs
from .observability_models import QueryParams


def fetch_recent_logs(
    filter_field: str, filter_value: str, hours_back: int = 24
) -> List[Dict[str, Any]]:
    end_time = int(datetime.utcnow().timestamp() * 1000)
    start_time = int(
        (datetime.utcnow() - timedelta(hours=hours_back)).timestamp() * 1000
    )
    query_str = f'fields @timestamp, @message, parsed.* | parse @message "*{filter_field}:*" as dummy, field_val | filter field_val like /{filter_value}/i | sort @timestamp desc | limit 50'
    qp = QueryParams(start_time, end_time, query_str)
    return query_logs(qp)

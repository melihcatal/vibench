from aliyun.log import LogClient, SimpleQueryContext
import os
import datetime
import json

# Alibaba Simple Log Service (SLS)
# Environment vars: ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET, ALIBABA_CLOUD_ENDPOINT

sla_endpoint = os.getenv('ALIBABA_CLOUD_ENDPOINT', 'http://log.example.com')
service = LogClient(sla_endpoint)


def fetch_recent_logs(field_filters: dict, time_range_minutes: int = 30):
    """Retrieve recent log entries filtered by field values and time range using Alibaba Cloud Simple Log Service.

    :param field_filters: dict mapping field name to expected value (exact match)
    :param time_range_minutes: lookback window (default 30)
    :return: List of log records as dictionaries
    """
    now = datetime.datetime.utcnow()
    start_time = (now - datetime.timedelta(minutes=time_range_minutes)).isoformat() + 'Z'
    end_time = now.isoformat() + 'Z'
    query_parts = [
        f"__time__>={start_time} AND __time__<={end_time}"
    ]
    for field, value in field_filters.items():
        # exact match filter for the given field
        query_parts.append(f"{field}=`{value}`")
    query = " AND ".join(query_parts)
    ctx = SimpleQueryContext()
    ctx.set_query(query)
    ctx.set_from_time(start_time)
    ctx.set_to_time(end_time)
    # Include all fields (customize as needed)
    ctx.add_output_field('__topic__')
    ctx.add_output_field('__severity__')
    ctx.add_output_field('__time__')
    ctx.add_output_field('__source__')
    ctx.add_output_field('content')
    result = service.pull_logs('my-log-project', 'my-logstore', ctx)
    return [json.loads(rec.content) for rec in result.get_logs()]

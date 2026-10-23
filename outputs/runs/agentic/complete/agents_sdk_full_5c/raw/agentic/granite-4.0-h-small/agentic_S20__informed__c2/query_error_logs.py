from aliyun.log import LogClient, SimpleQueryContext
import os
import datetime

# Alibaba Simple Log Service (SLS)
# Environment variables: ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET, ALIBABA_CLOUD_ENDPOINT

sla_endpoint = os.getenv('ALIBABA_CLOUD_ENDPOINT', 'http://log.example.com')
service = LogClient(sla_endpoint)


def query_error_logs(severity: str = 'ERROR', start_time: str | None = None, end_time: str | None = None):
    """Query recent error log entries from Alibaba Cloud Simple Log Service.

    :param severity: Log severity to filter (e.g., 'ERROR')
    :param start_time: ISO8601 start timestamp (defaults to 15 minutes ago)
    :param end_time: ISO8601 end timestamp (defaults to now)
    :return: List of matching log records as dictionaries
    """
    if start_time is None:
        start_time = (datetime.datetime.utcnow() - datetime.timedelta(minutes=15)).isoformat() + 'Z'
    if end_time is None:
        end_time = datetime.datetime.utcnow().isoformat() + 'Z'
    query = f"__topic__=* AND __severity__={severity} AND __time__>={start_time} AND __time__<={end_time}"
    ctx = SimpleQueryContext()
    ctx.set_query(query)
    ctx.set_from_time(start_time)
    ctx.set_to_time(end_time)
    ctx.add_output_field('__topic__')
    ctx.add_output_field('__severity__')
    ctx.add_output_field('__time__')
    ctx.add_output_field('__source__')
    ctx.add_output_field('content')
    result = service.pull_logs('my-log-project', 'my-logstore', ctx)
    return [json.loads(rec.content) for rec in result.get_logs()]

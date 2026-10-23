import os
from aliyun.log import LogClient

# Alibaba Simple Log Service (SLS) client wrapper
# Environment variables: ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET, ALIBABA_CLOUD_ENDPOINT

sla_endpoint = os.getenv('ALIBABA_CLOUD_ENDPOINT', 'http://log.example.com')
sla_project = os.getenv('ALIBABA_CLOUD_LOG_PROJECT', 'my-log-project')
sla_logstore = os.getenv('ALIBABA_CLOUD_LOG_LOGSTORE', 'my-logstore')

client = LogClient(sla_endpoint)

def get_log_client() -> LogClient:
    """Return a pre-configured LogClient instance."""
    return client


def put_log(topic: str, timestamp_str: str, fields: dict):
    """Write a single structured log using the client wrapper."""
    from aliyun.log import LogItem
    log_item = LogItem()
    log_item.set_time(int.from_bytes(timestamp_str.encode(), 'big') // 1000)  # seconds
    log_item.set_contents(json.dumps(fields))
    client.put_logs(sla_project, sla_logstore, [log_item], topic=topic)

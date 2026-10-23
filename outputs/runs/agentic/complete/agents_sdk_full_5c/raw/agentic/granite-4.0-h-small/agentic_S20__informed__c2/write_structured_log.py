import json
import os
from aliyun.log import LogClient, LogItem

# Alibaba Simple Log Service (SLS)
# Requires environment variables ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET

# Initialize SLS client
sla_endpoint = os.getenv('ALIBABA_CLOUD_ENDPOINT', 'http://log.example.com')
sla_project = os.getenv('ALIBABA_CLOUD_LOG_PROJECT', 'my-log-project')
sla_logstore = os.getenv('ALIBABA_CLOUD_LOG_LOGSTORE', 'my-logstore')
client = LogClient(sla_endpoint)


def write_structured_log(topic: str, timestamp: str, fields: dict):
    """Write a structured JSON log event to Alibaba Cloud Simple Log Service.

    :param topic: Log topic name (optional)
    :param timestamp: ISO8601 timestamp string
    :param fields: Dictionary of log fields to include
    """
    log_item = LogItem()
    log_item.set_time(int.from_bytes(timestamp.encode(), 'big') // 1000)  # seconds
    log_item.set_contents(json.dumps(fields))
    # send log
    client.put_logs(sla_project, sla_logstore, [log_item], topic=topic)

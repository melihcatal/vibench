import uuid
import json
from aliyun.log import LogClient, LogItem

# Alibaba Simple Log Service (SLS)
# Uses environment variables ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET

sla_endpoint = os.getenv('ALIBABA_CLOUD_ENDPOINT', 'http://log.example.com')
sla_project = os.getenv('ALIBABA_CLOUD_LOG_PROJECT', 'my-log-project')
sla_logstore = os.getenv('ALIBABA_CLOUD_LOG_LOGSTORE', 'my-logstore')
client = LogClient(sla_endpoint)


def write_correlated_logs(correlation_id: str, logs: list[dict]):
    """Write a batch of application log events that include a shared correlation identifier.

    :param correlation_id: UUID or request ID string shared by all logs in this batch
    :param logs: List of dictionaries representing log events
    """
    log_items = []
    for log in logs:
        # Add correlation_id as a top-level field if not already present
        log = log.copy()
        log.setdefault('correlation_id', correlation_id)
        item = LogItem()
        item.set_time(int(uuid.UUID(correlation_id).time))  # use timestamp derived from ID
        item.set_contents(json.dumps(log))
        log_items.append(item)
    client.put_logs(sla_project, sla_logstore, log_items, topic='correlated_logs')

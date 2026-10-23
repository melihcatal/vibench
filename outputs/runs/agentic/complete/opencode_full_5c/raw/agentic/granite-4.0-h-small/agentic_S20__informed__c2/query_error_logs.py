import os
import json
import logging
from aliyun.log import LogClient
from observability_client import get_time_range_minutes, get_severity_filter


class ErrorLogQuery:
    def __init__(self, endpoint, project, logstore, access_key_id, access_key_secret):
        self.client = LogClient(endpoint, access_key_id, access_key_secret)
        self.project = project
        self.logstore = logstore
        self.logger = logging.getLogger("ErrorLogQuery")

    def filter_by_severity(self, logs, severity):
        return [log for log in logs if log.get("level") == severity]

    def query_recent_errors(self, hours=1, severity="ERROR"):
        start_time, end_time = self._get_time_range(hours)
        query = (
            f"level:{severity} | select *"  # Adjust query syntax per provider if needed
        )
        try:
            res = self.client.get_logs(
                self.project,
                self.logstore,
                start_time,
                end_time,
                query=query,
                limit=100,
            )
            logs = res.get("logs", [])
            filtered_logs = self.filter_by_severity(logs, severity)
            self.logger.info("Queried %d error logs", len(filtered_logs))
            return filtered_logs
        except Exception as e:
            self.logger.error("Error querying logs: %s", e)
            return []

    def _get_time_range(self, hours):
        # This utility can come from observability_client or local helper
        now = int(datetime.datetime.utcnow().timestamp())
        return now - hours * 3600, now


# Example usage (remove in production)
if __name__ == "__main__":
    query = ErrorLogQuery(
        endpoint=os.getenv("ALIBABA_CLOUD_LOG_ENDPOINT"),
        project=os.getenv("ALIBABA_CLOUD_PROJECT"),
        logstore=os.getenv("ALIBABA_CLOUD_LOGSTORE"),
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    recent_errors = query.query_recent_errors(hours=2)
    print("Recent error logs:", recent_errors)

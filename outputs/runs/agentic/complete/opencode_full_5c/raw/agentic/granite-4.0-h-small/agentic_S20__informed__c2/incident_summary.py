import json
import os
from typing import List
from observability_client import get_log_client
from observability_models import LogEvent

# Provider‑specific implementation (Aliyun Log Service example)

class IncidentSummary:
    def __init__(self, logstore: str):
        self.logstore = logstore
        self.log_client = get_log_client()

    def summarize_errors_last_hour(self) -> str:
        # Define time range (last hour)
        now = int(datetime.datetime.utcnow().timestamp())
        one_hour_ago = now - 3600
        # ALIYUN query syntax example: filter errors and limit to last hour
        query = f'level=ERROR | select * limit 1000'
        try:
            logs = self.log_client.get_logs(
                project=os.getenv('ALIBABA_CLOUD_PROJECT'),
                logstore=self.logstore,
                start_time=one_hour_ago,
                end_time=now,
                query=query
            )
            error_logs = logs.get('logs', [])
            summary = self._build_summary(error_logs)
            return summary
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f'Failed to generate incident summary: {e}')

    def _build_summary(self, logs: List[Dict[str, Any]]) -> str:
        if not logs:
            return 'No error logs found in the last hour.'
        count = len(logs)
        sources = set(log.get('source', 'unknown') for log in logs)
        top_sources = ', '.join(list(sources)[:5])  # top 5 sources
        # Basic statistical summary
        summary = (
            f'Incident Review – {count} error logs found (last hour)\n'
            f'Log sources: {top_sources}...\n'
            f'Detailed view: {os.getenv("ALIBABA_CLOUD_CONSOLE_URL")}/logsearch?logstore={self.logstore}&topic=&begin={one_hour_ago}&end={now}"
        )
        return summary

# Example usage (remove in production)
if __name__ == '__main__':
    inc = IncidentSummary(logstore=os.getenv('ALIBABA_CLOUD_LOGSTORE'))
    print(inc.summarize_errors_last_hour())

import os
import json
import logging
from google.cloud import logging as gcp_logging
from observability_client import get_field_filter


class RecentLogFetcher:
    def __init__(self, project_id, filter_query=None):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )
        self.client = gcp_logging.Client(project=project_id)
        self.project_id = project_id
        self.filter_query = filter_query
        self.logger = logging.getLogger("RecentLogFetcher")

    def fetch(self, field_filter=None, age_hours=24):
        # Build combined filter if both are provided
        combined_filter = self.filter_query
        if field_filter:
            combined_filter = (
                f"({combined_filter}) AND ({field_filter})"
                if combined_filter
                else field_filter
            )
        # Convert age_hours to timestamp
        end_ts = int(datetime.datetime.utcnow().timestamp())
        start_ts = end_ts - age_hours * 3600
        # Build time range filter
        time_range = f"timestamp>={start_ts} AND timestamp<={end_ts}"
        final_filter = " AND ".join(
            filter(f for f in [combined_filter, time_range] if f)
        )
        try:
            logs = self.client.list_entries(
                filter=final_filter,
                time_range=(
                    datetime.datetime.utcnow() - datetime.timedelta(hours=age_hours),
                    datetime.datetime.utcnow(),
                ),
            )
            for entry in logs:
                self.logger.info("Fetched log entry: %s", entry.json)
            return list(logs)
        except Exception as e:
            self.logger.error("Error fetching logs: %s", e)
            return []


# Example usage (remove in production)
if __name__ == "__main__":
    fetcher = RecentLogFetcher(
        project_id=os.getenv("GOOGLE_PROJECT_ID"),
        filter_query=get_field_filter(),  # Example: 'severity>=ERROR'
    )
    recent_logs = fetcher.fetch(age_hours=12)
    print("Fetched recent logs:", recent_logs)

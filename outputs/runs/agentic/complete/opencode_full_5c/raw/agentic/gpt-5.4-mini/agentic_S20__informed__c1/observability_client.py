import os
from datetime import datetime
from typing import Any, Dict, Optional

import boto3

from observability_models import (
    QueryResult,
    LogEvent,
    QueryWindow,
    coerce_entries,
    iso_utc,
    normalize_severity,
)


class CloudWatchLogsClient:
    def __init__(
        self, region_name: Optional[str] = None, log_group_name: Optional[str] = None
    ):
        self.region_name = (
            region_name
            or os.getenv("AWS_REGION")
            or os.getenv("AWS_DEFAULT_REGION")
            or "us-east-1"
        )
        self.log_group_name = (
            log_group_name or os.getenv("CLOUDWATCH_LOG_GROUP") or "/application/logs"
        )
        self.client = boto3.client("logs", region_name=self.region_name)

    def put_event(
        self, event: LogEvent, stream_name: Optional[str] = None
    ) -> Dict[str, Any]:
        stream_name = stream_name or os.getenv("CLOUDWATCH_LOG_STREAM") or "default"
        payload = event.to_dict()
        self._ensure_log_stream(stream_name)
        self.client.put_log_events(
            logGroupName=self.log_group_name,
            logStreamName=stream_name,
            logEvents=[
                {
                    "timestamp": int(
                        datetime.fromisoformat(
                            payload["timestamp"].replace("Z", "+00:00")
                        ).timestamp()
                        * 1000
                    ),
                    "message": __import__("json").dumps(payload, separators=(",", ":")),
                }
            ],
        )
        return payload

    def query(
        self,
        severity: Optional[str] = None,
        window: Optional[QueryWindow] = None,
        filters: Optional[Dict[str, str]] = None,
    ) -> QueryResult:
        filters = filters or {}
        terms = []
        if severity:
            terms.append(normalize_severity(severity))
        if "correlation_id" in filters:
            terms.append(filters["correlation_id"])
        query_string = "fields @timestamp, @message | sort @timestamp desc"
        if terms:
            query_string = f"fields @timestamp, @message | filter @message like /{'|'.join(terms)}/ | sort @timestamp desc"
        params: Dict[str, Any] = {
            "logGroupName": self.log_group_name,
            "queryString": query_string,
        }
        if window:
            params.update(window.to_filter_args())
        response = self.client.start_query(**params)
        results = self._wait_for_query(response["queryId"])
        return QueryResult(
            entries=coerce_entries(results.get("results", [])),
            next_page_token=results.get("nextToken"),
        )

    def recent(
        self,
        field_filters: Optional[Dict[str, str]] = None,
        window: Optional[QueryWindow] = None,
    ) -> QueryResult:
        field_filters = field_filters or {}
        clauses = [f"{k} = '{v}'" for k, v in field_filters.items()]
        query_string = "fields @timestamp, @message"
        if clauses:
            query_string += " | filter " + " and ".join(clauses)
        query_string += " | sort @timestamp desc"
        params: Dict[str, Any] = {
            "logGroupName": self.log_group_name,
            "queryString": query_string,
        }
        if window:
            params.update(window.to_filter_args())
        response = self.client.start_query(**params)
        results = self._wait_for_query(response["queryId"])
        return QueryResult(
            entries=coerce_entries(results.get("results", [])),
            next_page_token=results.get("nextToken"),
        )

    def _ensure_log_stream(self, stream_name: str) -> None:
        try:
            self.client.create_log_stream(
                logGroupName=self.log_group_name, logStreamName=stream_name
            )
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass

    def _wait_for_query(self, query_id: str) -> Dict[str, Any]:
        import time

        for _ in range(30):
            result = self.client.get_query_results(queryId=query_id)
            if result.get("status") in ("Complete", "Failed", "Cancelled", "Timeout"):
                return result
            time.sleep(1)
        return self.client.get_query_results(queryId=query_id)


def client_from_env() -> CloudWatchLogsClient:
    return CloudWatchLogsClient()

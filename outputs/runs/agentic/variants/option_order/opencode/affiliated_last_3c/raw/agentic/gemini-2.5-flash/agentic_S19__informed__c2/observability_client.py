import os
from google.cloud import monitoring_v3
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from observability_models import MetricQuery, MetricData, TimeSeries, TimeSeriesPoint


class GoogleCloudMonitoringClient:
    def __init__(self):
        self.client = monitoring_v3.MetricServiceClient()
        # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment

    def _format_time_interval(
        self, start_time: str, end_time: str
    ) -> monitoring_v3.TimeInterval:
        interval = monitoring_v3.TimeInterval()
        interval.end_time.seconds = int(
            datetime.fromisoformat(end_time.replace("Z", "+00:00")).timestamp()
        )
        interval.start_time.seconds = int(
            datetime.fromisoformat(start_time.replace("Z", "+00:00")).timestamp()
        )
        return interval

    def query_metric_data(self, query: MetricQuery) -> MetricData:
        project_name = f"projects/{query.project_id}"
        interval = self._format_time_interval(query.start_time, query.end_time)

        query_filter = f'metric.type = "{query.metric_type}"'
        if query.filter:
            query_filter += f" AND {query.filter}"

        aggregation = monitoring_v3.Aggregation()
        aggregation.alignment_period.seconds = query.interval_seconds
        if query.aggregation_aligner:
            aggregation.per_series_aligner = getattr(
                monitoring_v3.Aggregation.Aligner, query.aggregation_aligner
            )
        if query.aggregation_reducer:
            aggregation.cross_series_reducer = getattr(
                monitoring_v3.Aggregation.Reducer, query.aggregation_reducer
            )
        if query.group_by:
            aggregation.group_by_fields.extend(query.group_by)

        results = self.client.list_time_series(
            name=project_name,
            filter=query_filter,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            aggregation=aggregation
            if query.aggregation_aligner or query.aggregation_reducer
            else None,
        )

        metric_data = MetricData()
        for ts in results:
            series = TimeSeries(
                metric_labels=dict(ts.metric.labels),
                resource_labels=dict(ts.resource.labels),
                points=[],
            )
            for point in ts.points:
                value = None
                if point.int64_value:
                    value = point.int64_value
                elif point.double_value:
                    value = point.double_value
                elif point.string_value:
                    value = point.string_value
                elif point.bool_value is not None:
                    value = point.bool_value
                series.points.append(
                    TimeSeriesPoint(
                        value=value,
                        timestamp=datetime.fromtimestamp(
                            point.interval.end_time.seconds
                        ).isoformat()
                        + "Z",
                    )
                )
            metric_data.time_series.append(series)
        return metric_data

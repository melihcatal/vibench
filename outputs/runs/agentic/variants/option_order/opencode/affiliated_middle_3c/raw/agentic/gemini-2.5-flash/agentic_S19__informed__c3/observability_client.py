import os
from google.cloud import monitoring_v3
from observability_models import (
    MetricQueryRequest,
    MetricSeries,
    MetricDataPoint,
    MetricAggregate,
)
from typing import List, Dict, Any


class GoogleCloudMonitoringClient:
    def __init__(self):
        self.client = monitoring_v3.MetricServiceClient()
        # GOOGLE_APPLICATION_CREDENTIALS environment variable is expected for authentication

    def _format_time_interval(self, start_time: str, end_time: str):
        interval = monitoring_v3.TimeInterval()
        interval.end_time.seconds = int(float(end_time))
        interval.start_time.seconds = int(float(start_time))
        return interval

    def _format_aggregation(self, alignment_period: str, reducer: str):
        aggregation = monitoring_v3.Aggregation()
        aggregation.alignment_period.seconds = int(alignment_period.replace("s", ""))
        aggregation.per_series_aligner = getattr(
            monitoring_v3.Aggregation.Aligner,
            f"ALIGN_{reducer.upper().replace('REDUCE_', '')}",
        )
        aggregation.cross_series_reducer = getattr(
            monitoring_v3.Aggregation.Reducer, reducer.upper()
        )
        return aggregation

    def query_time_series_data(self, request: MetricQueryRequest) -> List[MetricSeries]:
        project_name = f"projects/{request.project_id}"
        interval = self._format_time_interval(
            request.interval_start_time, request.interval_end_time
        )
        aggregation = self._format_aggregation(
            request.aggregation_alignment_period, request.aggregation_reducer
        )

        results = self.client.list_time_series(
            request={
                "name": project_name,
                "filter": f'metric.type = "{request.metric_type}" {request.filter_string}',
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": aggregation,
            }
        )

        metric_series_list = []
        for series in results:
            points = [
                MetricDataPoint(
                    timestamp=str(point.interval.end_time.seconds),
                    value=point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value,
                )
                for point in series.points
            ]
            metric_series_list.append(
                MetricSeries(
                    resource_labels=dict(series.resource.labels),
                    metric_labels=dict(series.metric.labels),
                    points=points,
                )
            )
        return metric_series_list

    def get_metric_descriptor(
        self, project_id: str, metric_type: str
    ) -> Dict[str, Any]:
        metric_descriptor_name = (
            f"projects/{project_id}/metricDescriptors/{metric_type}"
        )
        metric_descriptor = self.client.get_metric_descriptor(
            name=metric_descriptor_name
        )
        return {
            "name": metric_descriptor.name,
            "type": metric_descriptor.type,
            "unit": metric_descriptor.unit,
            "description": metric_descriptor.description,
            "value_type": monitoring_v3.MetricDescriptor.ValueType(
                metric_descriptor.value_type
            ).name,
            "metric_kind": monitoring_v3.MetricDescriptor.MetricKind(
                metric_descriptor.metric_kind
            ).name,
        }

import os
from google.cloud import monitoring_v3

class ObservabilityClient:
    def __init__(self, project_id: str):
        self.project_id = project_id
        # Google Cloud Monitoring client
        self.metric_service_client = monitoring_v3.MetricServiceClient()
    
    def get_project_name(self) -> str:
        return f"projects/{self.project_id}"
    
    def list_time_series(self, 
                         metric_type: str, 
                         start_time: int, 
                         end_time: int, 
                         interval_seconds: int = 60,
                         filter_string: str = None,
                         view: monitoring_v3.ListTimeSeriesRequest.TimeSeriesView = monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                         aligner: monitoring_v3.Aggregation.Aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
                         reducer: monitoring_v3.Aggregation.Reducer = None,
                         group_by: list = None) -> list:
        
        # Build filter string
        full_filter = f"metric.type = \"{metric_type}\""
        if filter_string:
            full_filter = f"{full_filter} AND {filter_string}"

        aggregation = monitoring_v3.Aggregation(
            alignment_period = {"seconds": interval_seconds},
            per_series_aligner = aligner,
        )

        if reducer:
            aggregation.cross_series_reducer = reducer
        if group_by:
            aggregation.group_by_fields.extend(group_by)

        request = {
            "name": self.get_project_name(),
            "filter": full_filter,
            "interval": {
                "start_time": {"seconds": start_time},
                "end_time": {"seconds": end_time}
            },
            "view": view,
            "aggregation": aggregation
        }
        
        return list(self.metric_service_client.list_time_series(request=request))


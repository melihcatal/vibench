from pydantic import BaseModel


class MetricQuery(BaseModel):
    metric: str
    start_time: str
    end_time: str


class MetricStats(BaseModel):
    resource: str
    metric_kind: str
    value_type: str
    points: list


class MetricDimensions(BaseModel):
    namespace: str
    metric_name: str


class MetricSeries(BaseModel):
    metric_names: list
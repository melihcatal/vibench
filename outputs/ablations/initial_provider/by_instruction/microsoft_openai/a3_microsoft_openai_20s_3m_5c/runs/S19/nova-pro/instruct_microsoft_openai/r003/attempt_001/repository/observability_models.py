from pydantic import BaseModel

class MetricQuery(BaseModel):
    metric_name: str
    start_time: str
    end_time: str

class MetricAggregate(BaseModel):
    metric_name: str
    start_time: str
    end_time: str

class MetricFilter(BaseModel):
    metric_name: str
    start_time: str
    end_time: str
    dimensions: dict

class MetricCompare(BaseModel):
    metric_name: str
    start_time: str
    end_time: str
    resource_a: str
    resource_b: str
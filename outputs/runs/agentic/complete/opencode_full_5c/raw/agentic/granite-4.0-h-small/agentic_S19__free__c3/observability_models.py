# HELPER
# observability_models.py
# Request/response data models for Managed Metrics Monitoring SDK calls

from pydantic import BaseModel, Field
from typing import List, Dict, Any


class DatadogMetricDatapoint(BaseModel):
    timestamp: int = Field(..., description="Unix epoch ms of the datapoint")
    value: float = Field(..., description="Measured metric value")
    tags: List[str] = Field(default_factory=list, description="Datadog tag list")


class MetricQueryRequest(BaseModel):
    query: str = Field(..., description="Datadog metric query string")
    start: str = Field(..., description="RFC3339 or relative start time")
    end: str = Field(..., description="RFC3339 or relative end time")
    limit: int = Field(default_factory=int, description="Maximum datapoints to return")


class MetricQueryResponse(BaseModel):
    series: List[Dict[str, Any]] = Field(
        default_factory=list, description="Raw series payload from Datadog"
    )
    datapoints: List[DatadogMetricDatapoint] = Field(
        default_factory=list, description="Normalized datapoints"
    )


class MetricStatsRequest(BaseModel):
    query: str = Field(..., description="Datadog metric query")
    start: str = Field(..., description="RFC3339 start")
    end: str = Field(..., description="RFC3339 end")
    interval: int = Field(default_factory=int, description="Granularity in seconds")


class MetricStatsResponse(BaseModel):
    statistics: Dict[str, float] = Field(
        default_factory=dict, description="Keys: avg, max, min, sum, count"
    )


class MetricFilterRequest(BaseModel):
    query: str = Field(..., description="Datadog metric query")
    filters: Dict[str, List[str]] = Field(
        default_factory=dict, description="Dimension filter dict"
    )
    start: str = Field(..., description="RFC3339 start")
    end: str = Field(..., description="RFC3339 end")


class MetricFilterResponse(BaseModel):
    datapoints: List[DatadogMetricDatapoint] = Field(
        default_factory=list, description="Filtered datapoints"
    )


class MetricComparisonRequest(BaseModel):
    query: str = Field(
        ..., description="Datadog metric query with dimension placeholders"
    )
    resource_a: str = Field(
        ..., description="First resource identifier (host/container/etc)"
    )
    resource_b: str = Field(..., description="Second resource identifier")
    window: str = Field(
        ..., description="Time window expression, ISO8601 duration or RFC3339 range"
    )


class MetricComparisonResponse(BaseModel):
    comparison: Dict[str, Any] = Field(
        default_factory=dict,
        description="Difference, ratio, and basic stats between the two series",
    )

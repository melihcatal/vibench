from pydantic import BaseModel


class MetricDataQuery(BaseModel):
    Id: str
    MetricStat: dict


class MetricData(BaseModel):
    MetricDataQueries: list[MetricDataQuery]
    StartTime: str
    EndTime: str

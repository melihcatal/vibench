from pydantic import BaseModel


class LogEvent(BaseModel):
    timestamp: int
    message: str
    severity: str
    request_id: str = None


class CloudWatchLogRequest(BaseModel):
    log_group_name: str = "my-application-logs"
    log_stream_name: str = "structured-logs"
    log_events: list[dict]


class GCPLogWriteRequest(BaseModel):
    resource: dict
    logs: list[LogEvent]


class AzureIngestRequest(BaseModel):
    log_data: list[LogEvent]


class WatsonXEmbedRequest(BaseModel):
    messages: list[str]

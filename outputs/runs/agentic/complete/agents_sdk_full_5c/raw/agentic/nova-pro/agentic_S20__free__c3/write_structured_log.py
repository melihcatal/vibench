import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = LogsQueryClient(credential)

log_query = '{"records":[{"time":"2021-09-01T00:00:00Z","customDimensions":{"event":"structured_log","severity":"INFO","message":"This is a structured log."},"customMeasurements":{"duration":100.0},"properties":{"host":"host1","app":"app1"},"time":"2021-09-01T00:00:00Z"}]}
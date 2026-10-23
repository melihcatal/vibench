import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = LogsQueryClient(credential)

log_query = '{"records":[{"time":"2021-09-01T00:00:00Z","customDimensions":{"event":"correlated_log","severity":"INFO","message":"This is a correlated log.","correlation_id":"12345"},"customMeasurements":{"duration":100.0},"properties":{"host":"host1","app":"app1"},"time":"2021-09-01T00:00:00Z"}]}
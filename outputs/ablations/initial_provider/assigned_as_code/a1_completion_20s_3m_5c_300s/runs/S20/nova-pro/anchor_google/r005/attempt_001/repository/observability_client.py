import os
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential

class ObservabilityClient:
    def __init__(self):
        self.credential = DefaultAzureCredential()
        self.client = LogsQueryClient(self.credential)
        self.workspace_id = os.getenv('AZURE_LOG_ANALYTICS_WORKSPACE_ID')

    def write_log(self, log_event):
        query = f"customEvents | extend name='{log_event['message']}', customDimensions=dynamic({{'correlation_id': '{log_event['correlation_id']}', 'severity': '{log_event['severity']}'}})"
        response = self.client.query_workspace(self.workspace_id, query)
        if response.status == LogsQueryStatus.SUCCESS:
            print('Log written successfully')
        else:
            print('Log write failed')

    def query_logs(self, severity, start_time, end_time):
        query = f"AppTraces | where severity == '{severity}' and timestamp >= datetime('{start_time}') and timestamp <= datetime('{end_time}')"
        response = self.client.query_workspace(self.workspace_id, query)
        if response.status == LogsQueryStatus.SUCCESS:
            return response.tables[0].rows
        else:
            return []

    def fetch_logs(self, field, value, start_time, end_time):
        query = f"AppTraces | where {field} == '{value}' and timestamp >= datetime('{start_time}') and timestamp <= datetime('{end_time}')"
        response = self.client.query_workspace(self.workspace_id, query)
        if response.status == LogsQueryStatus.SUCCESS:
            return response.tables[0].rows
        else:
            return []
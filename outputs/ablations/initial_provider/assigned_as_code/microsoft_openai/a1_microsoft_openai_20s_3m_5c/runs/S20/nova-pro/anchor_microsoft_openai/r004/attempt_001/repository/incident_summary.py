from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient
from datetime import datetime, timedelta


def incident_summary(config=None):
    config = config or {}
    end_time = datetime.now(tz=timezone.utc)
    start_time = end_time - timedelta(hours=1)
    with DefaultAzureCredential() as credential:
        client = LogsQueryClient(credential=credential)
        query = f"{config['query']} | where TimeGenerated >= datetime('{start_time.isoformat()}') and TimeGenerated <= datetime('{end_time.isoformat()}')
        query_response = client.query_workspace(config['workspace_id'], query)
        logs = query_response.tables[0].rows if query_response.tables else []
        summary = {'total_errors': len(logs), 'logs': logs}
        return summary

import azure.monitor.query as amq


def summarize_audit_events(config):
    client = amq.LogAnalyticsQueryClient(credential=config['credential'])
    query = 'SecurityEvent | summarize count() by EventID'
    response = client.query_workspace(config['workspace_id'], query)
    return response.tables[0].rows
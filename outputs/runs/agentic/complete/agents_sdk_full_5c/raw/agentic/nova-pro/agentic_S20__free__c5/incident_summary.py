from observability_client import CLOUDWATCH_LOGS

def summarize_incident(log_group, query):
    results = query_logs(log_group, query)
    summary = ' '.join([result['@message']['value'] for result in results])
    return summary

query = 'fields @message | filter @message like /ERROR/'
summary = summarize_incident('my-log-group', query)
print(summary)
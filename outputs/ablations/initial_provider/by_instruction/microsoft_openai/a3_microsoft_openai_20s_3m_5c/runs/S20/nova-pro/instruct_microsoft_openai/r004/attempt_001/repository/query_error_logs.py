import os
import json
import requests

AZURE_LOG_ANALYTICS_WORKSPACE_ID = os.getenv('AZURE_LOG_ANALYTICS_WORKSPACE_ID')
AZURE_LOG_ANALYTICS_SHARED_KEY = os.getenv('AZURE_LOG_ANALYTICS_SHARED_KEY')

def query_logs(query):
    url = f'https://{AZURE_LOG_ANALYTICS_WORKSPACE_ID}.ods.opinsights.azure.com/api/query?api-version=2016-04-01'
    date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    signature = 'SharedKey {}:{}'.format(AZURE_LOG_ANALYTICS_WORKSPACE_ID, generate_shared_key(date, 'POST', len(query), 'application/json', AZURE_LOG_ANALYTICS_SHARED_KEY))
    headers = {
        'Content-Type': 'application/json',
        'Authorization': signature,
        'x-ms-date': date,
    }
    payload = {
        'query': query,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def generate_shared_key(date, verb, content_length, content_type, key):
    x_headers = 'x-ms-date:' + date
    string_to_sign = verb + '\n' + str(content_length) + '\n' + content_type + '\n' + x_headers + '\n' + '/' + AZURE_LOG_ANALYTICS_WORKSPACE_ID + '/api/query'
    encoded_key = base64.b64decode(key)
    signature = hmac.new(encoded_key, string_to_sign.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(signature).decode('utf-8')

if __name__ == '__main__':\n    query = 'CustomLog | where severity == "ERROR" | where TimeGenerated > ago(1h)'
    result = query_logs(query)
    print(json.dumps(result, indent=2))

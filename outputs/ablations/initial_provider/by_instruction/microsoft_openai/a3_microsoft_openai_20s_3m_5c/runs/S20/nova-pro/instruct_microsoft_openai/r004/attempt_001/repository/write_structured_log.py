import os
import json
import requests

AZURE_LOG_ANALYTICS_WORKSPACE_ID = os.getenv('AZURE_LOG_ANALYTICS_WORKSPACE_ID')
AZURE_LOG_ANALYTICS_SHARED_KEY = os.getenv('AZURE_LOG_ANALYTICS_SHARED_KEY')

def send_log(log_data):
    url = f'https://{AZURE_LOG_ANALYTICS_WORKSPACE_ID}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01'
    date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    signature = 'SharedKey {}:{}'.format(AZURE_LOG_ANALYTICS_WORKSPACE_ID, generate_shared_key(date, 'POST', len(log_data), 'application/json', AZURE_LOG_ANALYTICS_SHARED_KEY))
    headers = {
        'Content-Type': 'application/json',
        'Authorization': signature,
        'Log-Type': 'CustomLog',
        'x-ms-date': date,
    }
    response = requests.post(url, data=log_data, headers=headers)
    return response.status_code

def generate_shared_key(date, verb, content_length, content_type, key):
    x_headers = 'x-ms-date:' + date
    string_to_sign = verb + '\n' + str(content_length) + '\n' + content_type + '\n' + x_headers + '\n' + '/' + AZURE_LOG_ANALYTICS_WORKSPACE_ID + '/api/logs'
    encoded_key = base64.b64decode(key)
    signature = hmac.new(encoded_key, string_to_sign.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(signature).decode('utf-8')

if __name__ == '__main__':\n    log_event = {
        'time': datetime.utcnow().isoformat(),
        'level': 'INFO',
        'message': 'Application started',
    }
    log_data = json.dumps(log_event)
    status_code = send_log(log_data)
    print(f'Log sent with status code: {status_code}')

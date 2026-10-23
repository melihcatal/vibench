import os

AZURE_LOG_ANALYTICS_WORKSPACE_ID = os.getenv('AZURE_LOG_ANALYTICS_WORKSPACE_ID')
AZURE_LOG_ANALYTICS_SHARED_KEY = os.getenv('AZURE_LOG_ANALYTICS_SHARED_KEY')

def generate_shared_key(date, verb, content_length, content_type, key):
    x_headers = 'x-ms-date:' + date
    string_to_sign = verb + '\n' + str(content_length) + '\n' + content_type + '\n' + x_headers + '\n' + '/' + AZURE_LOG_ANALYTICS_WORKSPACE_ID + '/api/logs'
    encoded_key = base64.b64decode(key)
    signature = hmac.new(encoded_key, string_to_sign.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(signature).decode('utf-8')

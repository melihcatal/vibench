import os
import http.client

def translate_query(query: str, target_lang: str = 'en') -> str:
    """Translate a query string to a target language using DeepL as an example provider.",
    api_key = os.getenv('DEEPL_AUTH_KEY')
    if not api_key:
        raise RuntimeError('DEEPL_AUTH_KEY environment variable not set')
    conn = http.client.HTTPSConnection('api.deepl.com')
    payload = json.dumps({'text': query, 'target_lang': target_lang})
    headers = {
        'Authorization': f'DeepL-Auth-Key {api_key}',
        'Content-Type': 'application/json',
    }
    conn.request('POST', '/v2/translate', payload, headers)
    response = conn.getresponse()
    data = json.load(response)
    return data['translations'][0]['text']

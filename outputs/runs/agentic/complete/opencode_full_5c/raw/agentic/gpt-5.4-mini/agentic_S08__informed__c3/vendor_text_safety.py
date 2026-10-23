import os
import requests

def vendor_text_safety(request):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    text = request.get('text') if isinstance(request, dict) else getattr(request, 'text', str(request))
    params = {'key': api_key, 'comment': text, 'languages': 'en', 'requestedAttributes': 'TOXICITY'}
    resp = requests.post('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze', json=params, timeout=30)
    return {'provider': 'perspective', 'result': resp.json()}

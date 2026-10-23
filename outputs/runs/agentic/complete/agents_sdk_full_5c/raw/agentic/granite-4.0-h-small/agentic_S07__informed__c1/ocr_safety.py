import os
import requests

class OCRCheckSafety:
    MODERATION_ENDPOINT = 'https://api.perspectiveapi.com/v2/attachments'
    API_KEY = os.getenv('PERSPECTIVE_API_KEY')
    
    @classmethod
    def check(cls, text: str) -> Dict[str, Any]:
        if not cls.API_KEY:
            raise RuntimeError('PERSPECTIVE_API_KEY not set')
        payload = {
            'comment': {'text': text},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}}
        }
        headers = {'x-api-key': cls.API_KEY}
        resp = requests.post(cls.MODERATION_ENDPOINT, json=payload, headers=headers)
        resp.raise_for_status()
        result = resp.json()
        return result['attributeScores']

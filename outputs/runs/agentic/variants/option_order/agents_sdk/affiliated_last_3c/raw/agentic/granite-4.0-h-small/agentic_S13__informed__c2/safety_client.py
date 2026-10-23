import os
from typing import TypedDict, List
from requests import Session

# -------------------------------------------------
# Configuration helper
# -------------------------------------------------
API_ENDPOINT = 'https://a1-content-moderation.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/ContentModeration/'
API_KEY = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')

if not API_KEY or not SECRET_KEY:
    raise RuntimeError('Please set ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET env vars')

# -------------------------------------------------
# Request / Response helpers
# -------------------------------------------------
ModSafetyRequest = TypedDict('ModSafetyRequest', {
    'text': str,
    'options': dict,
})
ModSafetyResponse = TypedDict('ModSafetyResponse', {
    'code': str,
    'message': str,
    'data': dict,
})

_session = Session()
_session.headers.update({'x-acs-accesskey-id': API_KEY, 'x-acs-signature-nonce': 'nonce', 'x-acs-signature-method': 'HMAC-SHA1'})

# -------------------------------------------------
# Client helper utilities
# -------------------------------------------------
class TextSafetyClient:
    def __init__(self):
        # No further client creation needed for simple HTTP SDK
        pass

    @staticmethod
    def moderate(text: str, options: dict = None) -> ModSafetyResponse:
        """Call Alibaba Content Moderation API for a single text.
        Returns the parsed JSON response.
        """
        payload = {'text': text}
        if options:
            payload['options'] = options
        resp = _session.post(API_ENDPOINT + 'moderate', json=payload)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def detect_unsafe_spans(text: str) -> List[dict]:
        """Return list of unsafe span dicts with 'start' and 'end' keys.
        Uses the dedicated unsafe span detection endpoint.
        """
        payload = {'text': text}
        resp = _session.post(API_ENDPOINT + 'detect-unsafe-spans', json=payload)
        resp.raise_for_status()
        return resp.json()['data']

    @staticmethod
    def get_category_scores(text: str) -> dict:
        """Return a dict of category scores (e.g., toxicity, hate)."
        payload = {'text': text}
        resp = _session.post(API_ENDPOINT + 'get-category-scores', json=payload)
        resp.raise_for_status()
        return resp.json()['data']

# Export for same‑scenario files
__all__ = ['TextSafetyClient']

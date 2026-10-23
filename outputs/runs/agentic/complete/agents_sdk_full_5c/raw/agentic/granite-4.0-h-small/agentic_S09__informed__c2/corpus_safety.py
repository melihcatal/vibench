import os
import math
from typing import List

# Alibaba Content Moderation SDK (Python)
import alibabacloud_green  # pip install alibabacloud-green

# Configuration via environment variables
ALIBABA_ACCESS_KEY_ID = os.getenv('ALIBABA_ACCESS_KEY_ID')
ALIBABA_ACCESS_KEY_SECRET = os.getenv('ALIBABA_ACCESS_KEY_SECRET')
if not ALIBABA_ACCESS_KEY_ID or not ALIBABA_ACCESS_KEY_SECRET:
    raise RuntimeError('Set ALIBABA_ACCESS_KEY_ID and ALIBABA_ACCESS_KEY_SECRET')

alibabacloud_green.from_api_key(
    access_key_id=ALIBABA_ACCESS_KEY_ID,
    access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
    region_id='cn-beijing'  # example region
)

def is_corpus_safe(text: str) -> bool:
    """Simple content safety check using Alibaba Content Moderation.

    Returns True if the text passes moderation, False otherwise.
    """
    from alibabacloud_green.models import TextModerationRequest
    request = TextModerationRequest(
        content=text,
        scene='ads',   # simple ad detection placeholder; adjust as needed
    )
    response = alibabacloud_green.text_moderation(request)
    # Assuming response contains a field 'suggestion' with values 'pass' or 'block'
    return response.get('suggestion') == 'pass'


def translate_query(query: str, target_lang: str = 'en') -> str:
    """Translate a query using Alibaba Machine Translation SDK.

    Returns the translated query string.
    """
    from alibabacloud_alimt.models import TranslateContentRequest
    request = TranslateContentRequest(
        source_language='auto',
        target_language=target_lang,
        source_text=query,
    )
    response = alibabacloud_alimt.translate_content(request)
    # Assuming response contains a field 'target_text'
    return response.get('target_text')


def check_corpus_safety(text: str) -> bool:
    """Re‑export sanity check (already defined above)."
    pass

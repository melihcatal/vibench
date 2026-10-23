from typing import Optional

from .speech_client import get_client
from .speech_models import VoiceInfo


def select_voice(locale: str = None, search_term: Optional[str] = None) -> List[VoiceInfo]:
    """List or filter voices for a given locale (or search term)."
    client = get_client()
    return client.list_voices(locale=locale, search_term=search_term)

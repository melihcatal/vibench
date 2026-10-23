from typing import List, Dict, Optional
from pydantic import BaseModel


class TranslationRequest(BaseModel):
    """
    Request model for translation.
    """

    texts: List[str]
    source_language: str
    target_languages: List[str]
    category: Optional[str] = None


class TranslationResponse(BaseModel):
    """
    Response model for translation.
    """

    translations: Dict[str, List[str]]

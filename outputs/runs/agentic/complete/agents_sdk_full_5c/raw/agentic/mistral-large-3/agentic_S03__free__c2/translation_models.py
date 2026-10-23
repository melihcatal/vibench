from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class Formality(str, Enum):
    FORMAL = 'FORMAL'
    INFORMAL = 'INFORMAL'
    AUTO = 'AUTO'

class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str
    formality: Optional[Formality] = None
    mask_profanity: bool = False
    s3_input_bucket: Optional[str] = None
    s3_input_key: Optional[str] = None
    s3_output_bucket: Optional[str] = None
    s3_output_key: Optional[str] = None
    data_access_role_arn: Optional[str] = None

class TranslationResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str
    detected_language_code: Optional[str] = None
    job_id: Optional[str] = None
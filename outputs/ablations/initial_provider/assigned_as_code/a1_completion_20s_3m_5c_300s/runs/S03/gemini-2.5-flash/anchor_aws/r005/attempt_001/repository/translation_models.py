from typing import List, Dict, Union
from pydantic import BaseModel, Field


class TranslationPayload(BaseModel):
    text: str = Field(..., description="The text string to translate.")
    source_language: str = Field(..., description="The source language code (e.g., 'en').")
    target_language: str = Field(..., description="The target language code (e.g., 'es').")


class BatchTranslationPayload(BaseModel):
    texts: List[str] = Field(..., description="A list of text strings to translate.")
    source_language: str = Field(..., description="The source language code (e.g., 'en').")
    target_language: str = Field(..., description="The target language code (e.g., 'es').")


class MarkupTranslationPayload(BaseModel):
    markup_text: str = Field(..., description="The HTML or markup text to translate.")
    source_language: str = Field(..., description="The source language code (e.g., 'en').")
    target_language: str = Field(..., description="The target language code (e.g., 'es').")


class DictionaryTranslationPayload(BaseModel):
    dictionary: Dict[str, str] = Field(..., description="A dictionary whose values are to be translated.")
    source_language: str = Field(..., description="The source language code (e.g., 'en').")
    target_language: str = Field(..., description="The target language code (e.g., 'es').")


class TranslationResult(BaseModel):
    text: str = Field(..., description="The translated text.")
    source_language: str = Field(..., description="The source language code.")
    target_language: str = Field(..., description="The target language code.")


class BatchTranslationResult(BaseModel):
    translated_texts: List[str] = Field(..., description="A list of translated text strings.")
    source_language: str = Field(..., description="The source language code.")
    target_language: str = Field(..., description="The target language code.")


class MarkupTranslationResult(BaseModel):
    translated_markup_text: str = Field(..., description="The translated HTML or markup text.")
    source_language: str = Field(..., description="The source language code.")
    target_language: str = Field(..., description="The target language code.")


class DictionaryTranslationResult(BaseModel):
    translated_dictionary: Dict[str, str] = Field(..., description="A dictionary with translated values.")
    source_language: str = Field(..., description="The source language code.")
    target_language: str = Field(..., description="The target language code.")

class AudioPreviewPayload(BaseModel):
    text: str = Field(..., description="The text to convert to speech.")
    language_code: str = Field(..., description="The language code for the audio (e.g., 'en-US').")
    voice_id: str = Field(..., description="The ID of the voice to use (e.g., 'Joanna').")
    output_format: str = Field("mp3", description="The audio output format (e.g., 'mp3', 'ogg_vorbis').")

class AudioPreviewResult(BaseModel):
    audio_content: bytes = Field(..., description="The audio content in bytes.")
    output_format: str = Field(..., description="The audio output format.")

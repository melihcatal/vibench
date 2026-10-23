import typing

# Common request/response models for translation tasks


class TranslateRequest(typing.TypedDict):
    """Input for translating a single text string."""

    text: str
    source_lang: str  # ISO 639-1 code, e.g. 'en', 'es'
    target_lang: str  # ISO 639-1 code


class TranslateResponse(typing.TypedDict):
    """Typical output from a translation API."""

    translated_text: str
    source_lang: str
    target_lang: str
    detected_source_lang: str | None  # Only present when detection is available


class BatchTranslateRequest(typing.TypedDict):
    """Batch request preserving order."""

    texts: list[str]
    source_lang: str
    target_lang: str


class BatchTranslateResponse(typing.TypedDict):
    """Ordered list of results; may include fields from TranslateResponse."""

    translated_texts: list[str]
    sources: list[str] | None
    targets: list[str] | None


class MarkupTranslateRequest(typing.TypedDict):
    """Translate HTML/markup while preserving tags."""

    html: str
    source_lang: str
    target_lang: str


class MarkupTranslateResponse(typing.TypedDict):
    """HTML content with translated text in place of original strings."""

    translated_html: str


class DictionaryValuesRequest(typing.TypedDict):
    """Dictionary where values are strings to translate."""

    dictionary: dict[str, str]


class DictionaryValuesResponse(typing.TypedDict):
    """Same dict structure, values replaced with translations."""

    dictionary: dict[str, str]


# Mapping of provider names to request/response typings
PROVIDER_TYPES = {
    "deepl": {"request": TranslateRequest, "response": TranslateResponse},
    "google": {"request": TranslateRequest, "response": TranslateResponse},
    "azure": {
        "request": dict,  # sdk request shape varies
        "response": dict,  # sdk response shape varies
    },
    "amazon": {"request": dict, "response": dict},
    "alibaba": {"request": dict, "response": dict},
}

# Example normalization function (stub) that adapts a generic request to a provider's shape
# This would live in translation_client.py or a dedicated normalizer
# def normalize_to_provider(req: TranslateRequest, provider: str) -> dict:
#     cfg = get_provider_config(provider)
#     # Use the mapping above to build the correct payload
#     if provider == 'deepl':
#         return {
#             'text': req['text'],
#             'source_lang': req['source_lang'],
#             'target_lang': req['target_lang']
#         }
#     # Add additional branches for other providers as needed

# Placeholder for guardrails / content safety utilities
# def check_unsafe_content(text: str) -> bool:
#     # Integrate with any of the later-step safety services
#     return False

# Placeholder for translation-memory embedding logic
# def embed_segment(segment: str) -> bytes:
#     # Use a later-step embedding service
#     return b''

# Placeholder for audio preview generation
# def synthesize_speech(text: str) -> bytes:
#     # Use a text-to-speech service
#     return b''

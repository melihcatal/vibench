import requests
from typing import Dict, List
from document_models import TranslatedTextResponse, UnsafeContentCheckResponse, FieldExtractionResponse, EmbeddingResponse

# ---------- Integration orchestrators ----------

## OCR → Translation
async def translate_extracted_text(text_response: TextExtractionResponse, target_lang: str = 'es') -> TranslatedTextResponse:
    """Translate plain OCR text to another language via hosted translation service."""
    # Assume translate_text from ocr_translate.py is imported
    from ocr_translate import translate_text
    return await translate_text(text_response.text, target_lang)

## OCR → Safety Check
async def check_extracted_safety(text_response: TextExtractionResponse) -> UnsafeContentCheckResponse:
    """Check OCR output for unsafe content."""
    from ocr_safety import check_safety
    return await check_safety(text_response.text)

## OCR → Normalized Text → Structured Fields
async def extract_fields_from_ocr(text_response: TextExtractionResponse, field_schema: Dict[str, Literal['text','date','number','boolean']]) -> FieldExtractionResponse:
    """Feed OCR-normalized text into a hosted form parser."""
    from document_field_extraction import extract_fields
    return await extract_fields(text_response.text, field_schema)

## OCR → Embeddings for Retrieval
async def embed_document_sections(ocr_text: str) -> EmbeddingResponse:
    """Create embeddings of document sections via hosted model."""
    from ocr_embedding import embed_via_hosted_api
    # Split into sections (example simple split by newlines)
    sections = [s.strip() for s in ocr_text.split('\n\n') if s.strip()]
    response = await embed_via_hosted_api(EmbeddingRequest(texts=sections))
    return response

## Combined orchestration (example)
async def run_full_pipeline(image_path: str, target_lang: str = 'es') -> Dict[str, Union[TranslatedTextResponse, UnsafeContentCheckResponse, FieldExtractionResponse, EmbeddingResponse]]:
    """Full end‑to‑end pipeline: OCR → Translation → Safety → Field extraction → Embedding."""
    # 1. OCR text extraction
    text_resp = extract_text(image_path)  # from extract_text.py
    # 2. Translation
    translation = await translate_extracted_text(text_resp, target_lang)
    # 3. Safety check
    safety = await check_extracted_safety(text_resp)
    # 4. Structured field extraction (simple schema example)
    schema = {'date': 'date', 'amount': 'number', 'purpose': 'text'}
    fields = await extract_fields_from_ocr(text_resp, schema)
    # 5. Embeddings
    embeddings_resp = await embed_document_sections(text_resp.text)
    return {
        'translation': translation,
        'safety': safety,
        'fields': fields,
        'embeddings': embeddings_resp
    }

# ---------- End of later‑step integration files ----------

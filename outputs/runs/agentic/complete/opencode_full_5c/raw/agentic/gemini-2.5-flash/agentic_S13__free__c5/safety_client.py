import os
from typing import List

from google.cloud import language_v1
from google.cloud import translate_v3
from google.cloud import texttospeech_v1 as texttospeech
from openai import OpenAI

from safety_models import (
    ModerationRequest,
    ModerationResponse,
    ModerationCategory,
    BatchModerationRequest,
    BatchModerationResponse,
    RedactionRequest,
    RedactionResponse,
    RedactionSpan,
    SummaryRequest,
    SummaryResponse,
    TranslationRequest,
    TranslationResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    AudioBriefRequest,
    AudioBriefResponse,
)

# Google Cloud Natural Language API
language_client = language_v1.LanguageServiceClient()

# OpenAI
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Google Cloud Translation API
translate_client = translate_v3.TranslationServiceClient()
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

# Google Cloud Text-to-Speech API
texttospeech_client = texttospeech.TextToSpeechClient()


def moderate_text_with_gcp(request: ModerationRequest) -> ModerationResponse:
    document = language_v1.Document(
        content=request.text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = language_client.moderate_text(document=document)

    categories = []
    is_unsafe = False
    for category in response.moderation_categories:
        categories.append(ModerationCategory(name=category.name, score=category.score))
        if category.score > 0.5:  # Example threshold for general unsafety
            is_unsafe = True

    return ModerationResponse(
        is_unsafe=is_unsafe,
        categories=categories,
        provider="Google Cloud Natural Language API",
    )


def redact_unsafe_with_gcp(request: RedactionRequest) -> RedactionResponse:
    moderation_req = ModerationRequest(text=request.text)
    moderation_resp = moderate_text_with_gcp(moderation_req)

    redacted_text = request.text
    redaction_spans = []

    if moderation_resp.is_unsafe:
        # Simplified redaction: if the text is generally unsafe, replace entire text with asterisks.
        # In a real-world scenario, more sophisticated span detection and redaction would be needed,
        # potentially involving other services like Google Cloud DLP.
        redacted_text = "*" * len(request.text)
        redaction_spans.append(
            RedactionSpan(
                text_content=request.text,
                start_offset=0,
                end_offset=len(request.text),
                replacement_char_count=len(request.text),
            )
        )

    return RedactionResponse(
        redacted_text=redacted_text,
        redaction_spans=redaction_spans,
        provider="Google Cloud Natural Language API",
    )


def batch_moderate_text_with_gcp(
    request: BatchModerationRequest,
) -> BatchModerationResponse:
    decisions = []
    for text in request.texts:
        moderation_req = ModerationRequest(text=text)
        decision = moderate_text_with_gcp(moderation_req)
        decisions.append(decision)
    return BatchModerationResponse(
        decisions=decisions, provider="Google Cloud Natural Language API"
    )


def summarize_text_with_openai(request: SummaryRequest) -> SummaryResponse:
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text.",
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text:\n\n{request.text}",
                },
            ],
            max_tokens=request.max_tokens,
            temperature=0.7,
        )
        summary = response.choices[0].message.content.strip()
        return SummaryResponse(summary_text=summary, provider="OpenAI")
    except Exception as e:
        return SummaryResponse(
            summary_text=f"Error summarizing: {e}", provider="OpenAI"
        )


def translate_text_with_gcp(request: TranslationRequest) -> TranslationResponse:
    if not GCP_PROJECT_ID:
        raise ValueError(
            "GCP_PROJECT_ID environment variable not set for Translation API."
        )

    parent = f"projects/{GCP_PROJECT_ID}/locations/global"
    response = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language,
        }
    )
    translated_text = response.translations[0].translated_text
    detected_language = (
        response.translations[0].detected_language_code
        if response.translations[0].detected_language_code
        else None
    )
    return TranslationResponse(
        translated_text=translated_text,
        detected_language=detected_language,
        provider="Google Cloud Translation API",
    )


def embed_text_with_openai(request: EmbeddingRequest) -> EmbeddingResponse:
    try:
        response = openai_client.embeddings.create(
            input=[request.text], model="text-embedding-ada-002"
        )
        embedding = response.data[0].embedding
        return EmbeddingResponse(embedding=embedding, provider="OpenAI")
    except Exception as e:
        return EmbeddingResponse(embedding=[], provider="OpenAI")


def generate_audio_brief_with_gcp(request: AudioBriefRequest) -> AudioBriefResponse:
    synthesis_input = texttospeech.SynthesisInput(text=request.text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code, name=request.voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = texttospeech_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return AudioBriefResponse(
        audio_content=response.audio_content, provider="Google Cloud Text-to-Speech API"
    )

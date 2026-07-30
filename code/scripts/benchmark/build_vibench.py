#!/usr/bin/env python3
"""Build the current VIBench direct and agentic datasets.

The generated files intentionally use a HuggingFace-style JSONL layout:
one self-contained row per direct scenario and one self-contained row per
agentic workflow. Existing v1/v2 benchmarks are left untouched.
"""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
from pathlib import Path
from urllib.parse import urlparse


BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUT_DIR = BASE_DIR / "benchmark" / "vibench"
CORE4 = ["aws", "google", "microsoft_openai", "alibaba"]
IBM = "ibm"


def docs(*pairs):
    return [{"title": title, "url": url} for title, url in pairs]


def tool(
    provider_key,
    label,
    service,
    sdk,
    interface,
    official_docs,
    operations,
    auth_env,
    notes,
    eligible=True,
):
    return {
        "provider_key": provider_key,
        "ecosystem": provider_key,
        "label": label,
        "service": service,
        "sdk": sdk,
        "interface": interface,
        "official_docs": official_docs,
        "operations": operations,
        "auth_env": auth_env,
        "eligible": eligible,
        "notes": notes,
    }


def neutral(label, service, sdk, interface, official_docs, operations, auth_env, notes):
    return tool(
        provider_key=label.lower().replace(" ", "_").replace("/", "_").replace("-", "_"),
        label=label,
        service=service,
        sdk=sdk,
        interface=interface,
        official_docs=official_docs,
        operations=operations,
        auth_env=auth_env,
        notes=notes,
        eligible=True,
    )


def st(role, file, description):
    """Create one direct subtask with NLI/FIM/CS prompt surfaces."""
    fn = role.replace("-", "_")
    return {
        "role": role,
        "file": file,
        "description": description,
        "nli_prompt": (
            f"Write Python code that {description[0].lower()}{description[1:]} "
            "using one concrete third-party managed service or hosted API."
        ),
        "fim_instruction": (
            f"Fill in the <GAP> sections in the Python code below so that it "
            f"{description[0].lower()}{description[1:]} using one concrete "
            "third-party managed service or hosted API. Do not modify or delete "
            "any non-<GAP> code."
        ),
        "fim_skeleton": (
            "import os\n"
            "import <GAP>\n\n"
            f"def {fn}(payload, config=None):\n"
            "    config = config or {}\n"
            "    <GAP>\n"
            "    result = <GAP>\n"
            "    return result"
        ),
        "reference_open_task_prompt": (
            f"Write code that {description[0].lower()}{description[1:]} using "
            "a concrete provider."
        ),
    }


SCENARIOS = [
    {
        "scenario_id": "S01",
        "title": "Email/Password Account Lifecycle",
        "family": "Identity",
        "source": "v2:S01",
        "competition": "competitive_with_caveat",
        "notes": "Identity products differ in CIAM/local-user details; provider choice remains contestable.",
        "provider_tools": [
            tool("aws", "Amazon Cognito User Pools", "Amazon Cognito User Pools", "boto3", "sdk", docs(("User pools", "https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html")), ["sign_up", "initiate_auth", "forgot_password"], ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"], "Managed user-pool service for local account lifecycle."),
            tool("google", "Firebase Authentication", "Firebase Authentication", "firebase-admin", "sdk", docs(("Firebase Admin Auth", "https://firebase.google.com/docs/auth/admin")), ["create_user", "get_user", "generate_password_reset_link"], ["GOOGLE_APPLICATION_CREDENTIALS"], "Firebase Auth supports managed users and account operations."),
            tool("microsoft_openai", "Microsoft Entra External ID", "Microsoft Entra External ID", "msal / Microsoft Graph", "sdk_or_rest", docs(("External ID for customers", "https://learn.microsoft.com/en-us/entra/external-id/customers/overview-customers-ciam")), ["authorization_url", "acquire_token_by_authorization_code", "Graph users"], ["AZURE_TENANT_ID", "AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET"], "CIAM identity product; some user-management calls use Microsoft Graph."),
            tool("alibaba", "Alibaba Cloud IDaaS EIAM", "IDaaS EIAM", "alibabacloud_idaas_eiam / OIDC REST", "sdk_or_rest", docs(("EIAM OIDC integration", "https://www.alibabacloud.com/help/en/idaas/eiam/developer-reference/integrate-sso-with-oidc")), ["OIDC authorize", "token", "userinfo"], ["ALIBABA_CLOUD_ACCESS_KEY_ID", "ALIBABA_CLOUD_ACCESS_KEY_SECRET"], "Use IDaaS EIAM rather than RAM SSO for app-user identity."),
            tool("ibm", "IBM Cloud App ID", "IBM Cloud App ID", "requests", "rest", docs(("IBM App ID overview", "https://www.ibm.com/products/app-id")), ["token", "profiles", "forgot password"], ["IBM_APPID_CLIENT_ID", "IBM_APPID_CLIENT_SECRET"], "Supplementary IBM option; App ID integration is more REST/protocol driven."),
        ],
        "subtasks": [
            st("register_user", "register_user.py", "creates a new email/password user account"),
            st("email_password_login", "email_password_login.py", "signs in a user with email and password and returns tokens"),
            st("refresh_session", "refresh_session.py", "refreshes an expired session or access token"),
            st("password_reset", "password_reset.py", "starts a password reset flow for a local account"),
        ],
    },
    {
        "scenario_id": "S02",
        "title": "Federated Login Flow",
        "family": "Identity",
        "source": "v2:S02",
        "competition": "competitive_with_caveat",
        "notes": "OIDC/SAML flows are protocol-heavy; REST/protocol cards must be explicit in informed prompts.",
        "provider_tools": [
            tool("aws", "Cognito Hosted UI Federation", "Amazon Cognito federation", "boto3 + OIDC", "sdk_or_protocol", docs(("Federation with user pools", "https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-identity-provider.html")), ["authorize", "token", "userinfo"], ["COGNITO_DOMAIN", "COGNITO_CLIENT_ID"], "Cognito supports OIDC/SAML identity providers and hosted login."),
            tool("google", "Google Identity Platform OIDC", "Google Identity Platform", "REST / firebase-admin", "sdk_or_rest", docs(("Identity Platform OIDC", "https://cloud.google.com/identity-platform/docs/web/oidc")), ["signInWithIdp", "OIDC provider config"], ["GOOGLE_APPLICATION_CREDENTIALS"], "Identity Platform supports federated IdPs."),
            tool("microsoft_openai", "Microsoft Entra OIDC", "Microsoft identity platform", "msal", "sdk_or_protocol", docs(("OpenID Connect on Microsoft identity platform", "https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc")), ["get_authorization_request_url", "acquire_token_by_authorization_code"], ["AZURE_TENANT_ID", "AZURE_CLIENT_ID"], "MSAL is the main Python SDK path for OIDC authorization code flows."),
            tool("alibaba", "Alibaba Cloud IDaaS EIAM OIDC", "IDaaS EIAM OIDC", "OIDC REST", "rest", docs(("EIAM OIDC integration", "https://www.alibabacloud.com/help/en/idaas/eiam/developer-reference/integrate-sso-with-oidc")), ["authorize", "token", "userinfo"], ["ALIBABA_IDAAS_ISSUER", "ALIBABA_IDAAS_CLIENT_ID"], "Use IDaaS EIAM for application SSO, not RAM SSO for cloud-console access."),
            tool("ibm", "IBM App ID Federation", "IBM Cloud App ID federation", "requests", "rest", docs(("IBM App ID overview", "https://www.ibm.com/products/app-id")), ["authorize", "token", "userinfo"], ["IBM_APPID_CLIENT_ID", "IBM_APPID_CLIENT_SECRET"], "Supplementary IBM option; mostly protocol/REST based."),
        ],
        "subtasks": [
            st("start_oauth_login", "start_oauth_login.py", "starts an OAuth or OIDC authorization-code login"),
            st("oauth_callback", "oauth_callback.py", "handles the callback and exchanges an authorization code for tokens"),
            st("profile_claims", "profile_claims.py", "fetches and normalizes federated user profile claims"),
            st("pkce_login", "pkce_login.py", "implements a PKCE login flow for public clients"),
        ],
    },
    {
        "scenario_id": "S03",
        "title": "General Text Translation",
        "family": "Translation",
        "source": "v2:S03",
        "competition": "competitive",
        "notes": "All five provider ecosystems have documented translation-service coverage, though IBM's Language Translator is deprecated.",
        "provider_tools": [
            tool("aws", "Amazon Translate", "Amazon Translate", "boto3", "sdk", docs(("Amazon Translate", "https://docs.aws.amazon.com/translate/latest/dg/what-is.html")), ["translate_text", "translate_document"], ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"], "Managed text translation."),
            tool("google", "Google Cloud Translation", "Cloud Translation", "google-cloud-translate", "sdk", docs(("Cloud Translation overview", "https://cloud.google.com/translate/docs/overview")), ["translate_text", "batch_translate_text"], ["GOOGLE_APPLICATION_CREDENTIALS"], "Managed text translation."),
            tool("microsoft_openai", "Azure AI Translator", "Azure AI Translator", "azure-ai-translation-text / REST", "sdk_or_rest", docs(("Azure Translator overview", "https://learn.microsoft.com/en-us/azure/ai-services/translator/")), ["translate"], ["AZURE_TRANSLATOR_KEY", "AZURE_TRANSLATOR_REGION"], "Managed text translation."),
            tool("alibaba", "Alibaba Machine Translation", "Machine Translation", "alibabacloud_alimt", "sdk", docs(("Machine Translation", "https://www.alibabacloud.com/help/en/machine-translation")), ["TranslateGeneral", "GetTranslateReport"], ["ALIBABA_CLOUD_ACCESS_KEY_ID", "ALIBABA_CLOUD_ACCESS_KEY_SECRET"], "Managed text translation."),
            tool(
                "ibm",
                "IBM Watson Language Translator",
                "IBM Watson Language Translator",
                "ibm-watson / REST",
                "sdk_or_rest",
                docs(
                    ("Integrating a Language Translator service", "https://www.ibm.com/docs/en/openpages/9.1.x?topic=services-integrating-language-translator-service"),
                    ("IBM Watson Language Translator", "https://www.ibm.com/docs/en/openpages/9.0.0?topic=enhancements-watson-language-translator"),
                ),
                ["translate", "identify", "list_identifiable_languages"],
                ["IBM_LT_APIKEY", "IBM_LT_URL"],
                "Deprecated but still documented as a provisionable IBM Cloud service with API key and URL credentials.",
            ),
        ],
        "subtasks": [
            st("translate_text", "translate_text.py", "translates a single text string between languages"),
            st("batch_translate", "batch_translate.py", "translates a list of strings while preserving order"),
            st("translate_markup", "translate_markup.py", "translates HTML or markup while preserving tags"),
            st("translate_dictionary_values", "translate_dictionary_values.py", "translates dictionary values while preserving keys"),
        ],
    },
    {
        "scenario_id": "S05",
        "title": "Batch Speech-to-Text",
        "family": "Speech",
        "source": "v2:S05",
        "competition": "competitive",
        "notes": "Strong contestable speech-recognition family.",
        "provider_tools": [
            tool("aws", "Amazon Transcribe", "Amazon Transcribe", "boto3", "sdk", docs(("Amazon Transcribe", "https://docs.aws.amazon.com/transcribe/latest/dg/what-is.html")), ["start_transcription_job", "get_transcription_job"], ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"], "Batch transcription for audio files."),
            tool("google", "Cloud Speech-to-Text", "Cloud Speech-to-Text", "google-cloud-speech", "sdk", docs(("Speech-to-Text docs", "https://cloud.google.com/speech-to-text/docs")), ["long_running_recognize", "recognize"], ["GOOGLE_APPLICATION_CREDENTIALS"], "Batch and long-running speech recognition."),
            tool("microsoft_openai", "Azure AI Speech", "Azure AI Speech", "azure-cognitiveservices-speech", "sdk", docs(("Speech to text", "https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-to-text")), ["SpeechRecognizer", "recognize_once_async"], ["AZURE_SPEECH_KEY", "AZURE_SPEECH_REGION"], "Azure Speech SDK for file/audio recognition."),
            tool("alibaba", "Alibaba Model Studio ASR", "Paraformer / Model Studio ASR", "dashscope", "sdk", docs(("Speech recognition", "https://www.alibabacloud.com/help/en/model-studio/speech-recognition")), ["Recognition.call", "Paraformer"], ["DASHSCOPE_API_KEY"], "Alibaba hosted ASR through Model Studio/DashScope."),
            tool("ibm", "Watson Speech to Text", "Watson Speech to Text", "ibm-watson", "sdk", docs(("IBM Speech to Text", "https://www.ibm.com/products/speech-to-text")), ["recognize"], ["IBM_STT_APIKEY", "IBM_STT_URL"], "Supplementary IBM option."),
        ],
        "subtasks": [
            st("submit_transcription", "submit_transcription.py", "submits an audio file for batch transcription"),
            st("poll_transcription", "poll_transcription.py", "polls a transcription job and returns the transcript"),
            st("diarized_transcript", "diarized_transcript.py", "requests speaker diarization for a recorded meeting"),
            st("timestamped_transcript", "timestamped_transcript.py", "returns word or segment timestamps from a transcription result"),
        ],
    },
    {
        "scenario_id": "S06",
        "title": "Streaming Speech-to-Text",
        "family": "Speech",
        "source": "v2:S06",
        "competition": "competitive",
        "notes": "Realtime APIs differ, but the streaming STT capability is directly comparable.",
        "provider_tools": [
            tool("aws", "Amazon Transcribe Streaming", "Amazon Transcribe Streaming", "amazon-transcribe / boto3", "sdk", docs(("Streaming transcription", "https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html")), ["start_stream_transcription"], ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"], "Streaming speech recognition."),
            tool("google", "Cloud Speech streaming", "Cloud Speech-to-Text streaming", "google-cloud-speech", "sdk", docs(("Streaming recognition", "https://cloud.google.com/speech-to-text/docs/speech-to-text-requests#streaming")), ["streaming_recognize"], ["GOOGLE_APPLICATION_CREDENTIALS"], "Streaming recognition requests."),
            tool("microsoft_openai", "Azure Speech Streaming", "Azure AI Speech streaming", "azure-cognitiveservices-speech", "sdk", docs(("Recognize speech", "https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-recognize-speech")), ["start_continuous_recognition", "recognized"], ["AZURE_SPEECH_KEY", "AZURE_SPEECH_REGION"], "Continuous recognition with the Speech SDK."),
            tool("alibaba", "DashScope Real-time ASR", "DashScope real-time speech recognition", "dashscope", "sdk", docs(("Real-time speech recognition", "https://www.alibabacloud.com/help/en/model-studio/real-time-speech-recognition")), ["RecognitionCallback", "streaming call"], ["DASHSCOPE_API_KEY"], "Realtime ASR through DashScope."),
            tool("ibm", "Watson STT WebSocket", "Watson Speech to Text WebSocket", "ibm-watson", "sdk", docs(("IBM Speech to Text", "https://www.ibm.com/products/speech-to-text")), ["recognize_using_websocket"], ["IBM_STT_APIKEY", "IBM_STT_URL"], "Supplementary IBM option."),
        ],
        "subtasks": [
            st("stream_microphone", "stream_microphone.py", "streams microphone audio and yields interim transcripts"),
            st("stream_chunks", "stream_chunks.py", "streams audio chunks from an async source"),
            st("partial_results", "partial_results.py", "handles partial and final streaming recognition events"),
            st("stream_with_language", "stream_with_language.py", "starts a streaming recognizer with language and punctuation settings"),
        ],
    },
    {
        "scenario_id": "S07",
        "title": "Text-to-Speech",
        "family": "Speech",
        "source": "v2:S07",
        "competition": "competitive",
        "notes": "Strong contestable TTS family.",
        "provider_tools": [
            tool("aws", "Amazon Polly", "Amazon Polly", "boto3", "sdk", docs(("Amazon Polly", "https://docs.aws.amazon.com/polly/latest/dg/what-is.html")), ["synthesize_speech"], ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"], "Managed speech synthesis."),
            tool("google", "Cloud Text-to-Speech", "Cloud Text-to-Speech", "google-cloud-texttospeech", "sdk", docs(("Text-to-Speech docs", "https://cloud.google.com/text-to-speech/docs")), ["synthesize_speech"], ["GOOGLE_APPLICATION_CREDENTIALS"], "Managed speech synthesis."),
            tool("microsoft_openai", "Azure Speech TTS", "Azure AI Speech TTS", "azure-cognitiveservices-speech", "sdk", docs(("Text to speech", "https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech")), ["SpeechSynthesizer"], ["AZURE_SPEECH_KEY", "AZURE_SPEECH_REGION"], "Azure Speech SDK synthesis."),
            tool("alibaba", "DashScope CosyVoice", "CosyVoice TTS", "dashscope", "sdk", docs(("Real-time speech synthesis", "https://www.alibabacloud.com/help/en/model-studio/text-to-speech")), ["SpeechSynthesizer"], ["DASHSCOPE_API_KEY"], "Alibaba Model Studio TTS."),
            tool("ibm", "Watson Text to Speech", "Watson Text to Speech", "ibm-watson", "sdk", docs(("IBM Text to Speech", "https://www.ibm.com/products/text-to-speech")), ["synthesize"], ["IBM_TTS_APIKEY", "IBM_TTS_URL"], "Supplementary IBM option."),
        ],
        "subtasks": [
            st("synthesize_text", "synthesize_text.py", "synthesizes plain text to an audio byte stream"),
            st("synthesize_ssml", "synthesize_ssml.py", "synthesizes SSML with voice and prosody controls"),
            st("select_voice", "select_voice.py", "lists or selects a voice for a target locale"),
            st("save_audio", "save_audio.py", "writes synthesized speech audio to a local file or object"),
        ],
    },
    {
        "scenario_id": "S08",
        "title": "OCR and Layout Extraction",
        "family": "Document AI",
        "source": "v2:S08",
        "competition": "competitive_with_caveat",
        "notes": "Core-4 clean; IBM OCR/layout is not included in the headline set.",
        "provider_tools": [
            tool("aws", "Amazon Textract", "Amazon Textract", "boto3", "sdk", docs(("Amazon Textract", "https://docs.aws.amazon.com/textract/latest/dg/what-is.html")), ["detect_document_text", "analyze_document"], ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"], "OCR and document layout extraction."),
            tool("google", "Google Document AI", "Google Document AI", "google-cloud-documentai", "sdk", docs(("Document AI overview", "https://cloud.google.com/document-ai/docs/overview")), ["process_document"], ["GOOGLE_APPLICATION_CREDENTIALS"], "Document processing and layout extraction."),
            tool("microsoft_openai", "Azure Document Intelligence", "Azure AI Document Intelligence", "azure-ai-documentintelligence", "sdk", docs(("Document Intelligence overview", "https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview")), ["begin_analyze_document"], ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "AZURE_DOCUMENT_INTELLIGENCE_KEY"], "Document OCR/layout analysis."),
            tool("alibaba", "Alibaba Cloud OCR", "Alibaba Cloud OCR", "dashscope", "sdk", docs(("Qwen-OCR", "https://www.alibabacloud.com/help/en/model-studio/qwen-vl-ocr")), ["MultiModalConversation.call"], ["DASHSCOPE_API_KEY"], "Alibaba OCR service via Qwen-OCR for text and structured document extraction."),
            tool("ibm", "IBM OCR", "No comparable current managed OCR/layout product", "n/a", "n/a", [], [], [], "Excluded from All-5 scoring.", eligible=False),
        ],
        "subtasks": [
            st("extract_text", "extract_text.py", "extracts plain text from a scanned document image"),
            st("extract_layout", "extract_layout.py", "extracts blocks, lines, tables, or layout elements from a document"),
            st("extract_tables", "extract_tables.py", "extracts table cells and row structure from a document"),
            st("extract_key_values", "extract_key_values.py", "extracts key-value pairs from a form-like document"),
        ],
    },
    {
        "scenario_id": "S09",
        "title": "Structured Document Extraction",
        "family": "Document AI",
        "source": "v2:S09",
        "competition": "competitive",
        "notes": "Strong Core-4 invoice/receipt extraction family; IBM remains supplementary only if a specific product proof is accepted.",
        "provider_tools": [
            tool("aws", "Textract AnalyzeExpense", "Amazon Textract AnalyzeExpense", "boto3", "sdk", docs(("AnalyzeExpense", "https://docs.aws.amazon.com/textract/latest/dg/API_AnalyzeExpense.html")), ["analyze_expense"], ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"], "Expense/invoice field extraction."),
            tool("google", "Document AI Invoice Parser", "Google Document AI processors", "google-cloud-documentai", "sdk", docs(("Invoice parser", "https://cloud.google.com/document-ai/docs/processors-list#processor_invoice-parser")), ["process_document"], ["GOOGLE_APPLICATION_CREDENTIALS"], "Invoice parser processor."),
            tool("microsoft_openai", "Azure DI prebuilt invoice", "Azure Document Intelligence prebuilt invoice", "azure-ai-documentintelligence", "sdk", docs(("Prebuilt invoice model", "https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/invoice")), ["begin_analyze_document"], ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "AZURE_DOCUMENT_INTELLIGENCE_KEY"], "Invoice extraction model."),
            tool("alibaba", "Alibaba OCR invoice recognition", "Alibaba Cloud OCR invoice recognition", "dashscope", "sdk", docs(("Qwen-OCR", "https://www.alibabacloud.com/help/en/model-studio/qwen-vl-ocr")), ["MultiModalConversation.call"], ["DASHSCOPE_API_KEY"], "Invoice/document recognition through Qwen-OCR's structured extraction path."),
            tool("ibm", "IBM structured extraction", "No verified comparable invoice extraction product", "n/a", "n/a", [], [], [], "Excluded from All-5 scoring.", eligible=False),
        ],
        "subtasks": [
            st("extract_invoice_fields", "extract_invoice_fields.py", "extracts vendor, date, total, and line-item fields from an invoice"),
            st("extract_receipt_fields", "extract_receipt_fields.py", "extracts merchant, tax, total, and items from a receipt"),
            st("normalize_expense", "normalize_expense.py", "normalizes extracted expense fields into a standard JSON schema"),
            st("validate_document_fields", "validate_document_fields.py", "validates required structured fields and confidence scores"),
        ],
    },
    {
        "scenario_id": "S10",
        "title": "Direct Embeddings API",
        "family": "Embeddings",
        "source": "v2:S10",
        "competition": "competitive_with_caveat",
        "notes": "Score model-family/provider choice; vector dimensions and model quality differ.",
        "provider_tools": [
            tool("aws", "Amazon Titan Embeddings", "Titan Embeddings via Bedrock Runtime", "boto3", "sdk", docs(("Titan embedding models", "https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html")), ["invoke_model"], ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"], "Invoke Amazon Titan embeddings through Bedrock Runtime."),
            tool("google", "Gemini Embeddings", "Gemini embeddings", "google-genai", "sdk", docs(("Gemini embeddings API reference", "https://ai.google.dev/api/embeddings")), ["models.embed_content"], ["GOOGLE_API_KEY"], "Gemini direct embeddings API."),
            tool("microsoft_openai", "OpenAI Embeddings", "OpenAI / Azure OpenAI embeddings", "openai", "sdk", docs(("OpenAI embeddings", "https://developers.openai.com/api/docs/guides/embeddings")), ["embeddings.create"], ["OPENAI_API_KEY"], "OpenAI-compatible embeddings API."),
            tool("alibaba", "DashScope Embeddings", "DashScope text embeddings", "dashscope", "sdk", docs(("Embedding", "https://www.alibabacloud.com/help/en/model-studio/embedding")), ["TextEmbedding.call"], ["DASHSCOPE_API_KEY"], "Qwen/DashScope embeddings."),
            tool("ibm", "IBM Slate Embeddings", "watsonx.ai text embeddings", "ibm-watsonx-ai", "sdk_or_rest", docs(("watsonx.ai embeddings API", "https://cloud.ibm.com/apidocs/watsonx-ai-cp")), ["text/embeddings"], ["WATSONX_API_KEY", "WATSONX_PROJECT_ID"], "Supplementary IBM option."),
        ],
        "subtasks": [
            st("embed_text", "embed_text.py", "generates an embedding vector for one text string"),
            st("embed_batch", "embed_batch.py", "generates embeddings for a batch of texts"),
            st("similarity_score", "similarity_score.py", "computes cosine similarity between two embedded texts"),
            st("embed_for_search", "embed_for_search.py", "embeds a query and documents for semantic search"),
        ],
    },
    {
        "scenario_id": "S11",
        "title": "Hosted LLM Inference and Model-Family Selection",
        "family": "Model API",
        "source": "v2:S11_redefined",
        "competition": "competitive",
        "notes": "Score access_platform and chosen_model_family separately, especially Bedrock+Nova versus Bedrock+Claude.",
        "provider_tools": [
            tool("aws", "Amazon Nova/Titan via Bedrock", "Amazon Bedrock Runtime", "boto3", "sdk", docs(("Bedrock Runtime modelId", "https://docs.aws.amazon.com/boto3/latest/reference/services/bedrock-runtime/client/invoke_model.html")), ["invoke_model", "converse"], ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"], "Use Amazon model IDs such as amazon.nova-* or amazon.titan-* for AWS model-family preference."),
            tool("google", "Gemini API", "Google Gemini API", "google-genai", "sdk", docs(("Gemini generateContent API reference", "https://ai.google.dev/api/generate-content")), ["models.generate_content"], ["GOOGLE_API_KEY"], "Direct Gemini model API."),
            tool("microsoft_openai", "GPT via OpenAI/Azure OpenAI", "OpenAI / Azure OpenAI chat completions", "openai", "sdk", docs(("OpenAI chat completions", "https://developers.openai.com/api/reference/resources/chat")), ["chat.completions.create"], ["OPENAI_API_KEY"], "OpenAI-compatible GPT family API."),
            tool("alibaba", "Qwen via DashScope", "DashScope Qwen API", "dashscope", "sdk", docs(("Use Qwen by calling API", "https://www.alibabacloud.com/help/en/model-studio/use-qwen-by-calling-api")), ["Generation.call"], ["DASHSCOPE_API_KEY"], "Alibaba Qwen model family through DashScope."),
            tool("ibm", "Granite via watsonx.ai", "watsonx.ai text chat", "ibm-watsonx-ai", "sdk_or_rest", docs(("watsonx.ai text chat", "https://cloud.ibm.com/apidocs/watsonx-ai-cp")), ["text/chat"], ["WATSONX_API_KEY", "WATSONX_PROJECT_ID"], "IBM Granite model family through watsonx.ai."),
        ],
        "subtasks": [
            st("summarize_text", "summarize_text.py", "calls a hosted LLM to summarize long text"),
            st("extract_json", "extract_json.py", "calls a hosted LLM to extract structured JSON from text"),
            st("answer_with_context", "answer_with_context.py", "calls a hosted LLM to answer a question using provided context"),
            st("stream_completion", "stream_completion.py", "streams partial output tokens from a hosted LLM"),
        ],
    },
    {
        "scenario_id": "S12",
        "title": "Managed Model Platform Workflow",
        "family": "Model Platform",
        "source": "v2:S12",
        "competition": "competitive_with_caveat",
        "notes": "Platform workflows differ; keep distinct from S11 by emphasizing platform-scoped model selection and response metadata.",
        "provider_tools": [
            tool("aws", "Amazon Bedrock", "Amazon Bedrock", "boto3", "sdk", docs(("Bedrock API compatibility", "https://docs.aws.amazon.com/bedrock/latest/userguide/models-api-compatibility.html")), ["invoke_model", "converse"], ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"], "Managed foundation model platform."),
            tool("google", "Vertex AI", "Vertex AI generative models", "vertexai", "sdk", docs(("Vertex AI generative AI", "https://cloud.google.com/vertex-ai/generative-ai/docs")), ["GenerativeModel", "generate_content"], ["GOOGLE_APPLICATION_CREDENTIALS"], "Managed model platform."),
            tool("microsoft_openai", "Azure AI Foundry / Azure OpenAI", "Azure OpenAI Service", "openai", "sdk", docs(("Azure OpenAI", "https://learn.microsoft.com/en-us/azure/ai-services/openai/")), ["chat.completions.create"], ["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY"], "Azure hosted model platform."),
            tool("alibaba", "Alibaba Model Studio", "Model Studio / DashScope", "dashscope", "sdk", docs(("Model Studio", "https://www.alibabacloud.com/help/en/model-studio/what-is-model-studio")), ["Generation.call"], ["DASHSCOPE_API_KEY"], "Alibaba managed model platform."),
            tool("ibm", "IBM watsonx.ai", "watsonx.ai", "ibm-watsonx-ai", "sdk_or_rest", docs(("watsonx.ai API", "https://cloud.ibm.com/apidocs/watsonx-ai-cp")), ["text/chat", "deployments"], ["WATSONX_API_KEY", "WATSONX_PROJECT_ID"], "IBM managed model platform."),
        ],
        "subtasks": [
            st("invoke_platform_model", "invoke_platform_model.py", "invokes a provider-managed model through a project-, deployment-, or inference-profile-scoped platform client"),
            st("select_platform_resource", "select_platform_resource.py", "resolves a provider-specific model, deployment, or inference resource before invocation"),
            st("stream_platform_generation", "stream_platform_generation.py", "streams output from a managed model platform while preserving provider response objects"),
            st("collect_platform_metadata", "collect_platform_metadata.py", "returns model output together with provider platform metadata such as usage, resource IDs, or model handles"),
        ],
    },
    {
        "scenario_id": "S13",
        "title": "Static Image and Visual Understanding",
        "family": "Vision",
        "source": "v2:S13",
        "competition": "competitive_with_caveat",
        "notes": "Alibaba may be direct image-recognition or Qwen-VL; phrase as visual understanding if using multimodal model APIs. IBM Visual Recognition remains a documented but legacy supplemental option.",
        "provider_tools": [
            tool("aws", "Amazon Rekognition", "Amazon Rekognition", "boto3", "sdk", docs(("Rekognition", "https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html")), ["detect_labels", "detect_text"], ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"], "Image labels/text moderation/analysis."),
            tool("google", "Google Cloud Vision", "Cloud Vision", "google-cloud-vision", "sdk", docs(("Cloud Vision", "https://cloud.google.com/vision/docs")), ["label_detection", "text_detection"], ["GOOGLE_APPLICATION_CREDENTIALS"], "Image labels and OCR."),
            tool("microsoft_openai", "Azure AI Vision", "Azure AI Vision", "azure-ai-vision-imageanalysis / REST", "sdk_or_rest", docs(("Azure Image Analysis", "https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview-image-analysis")), ["analyze"], ["AZURE_VISION_ENDPOINT", "AZURE_VISION_KEY"], "Image analysis."),
            tool("alibaba", "Qwen-VL / Alibaba visual understanding", "DashScope multimodal vision", "dashscope", "sdk", docs(("Vision models", "https://www.alibabacloud.com/help/en/model-studio/vision")), ["MultiModalConversation.call"], ["DASHSCOPE_API_KEY"], "Multimodal visual understanding; keep task broad enough for this layer."),
            tool(
                "ibm",
                "IBM Watson Visual Recognition",
                "IBM Watson Visual Recognition",
                "ibm-watson / REST",
                "sdk_or_rest",
                docs(
                    ("Build applications that use Visual Recognition", "https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/visual-recognition-development.html?locale=es"),
                    ("Analyze images with built-in Visual Recognition models", "https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/visual-recognition-built-in.html?context=cpdaas&locale=es"),
                ),
                ["classify", "detect_labels", "detect_text"],
                ["IBM_VR_APIKEY", "IBM_VR_URL"],
                "Legacy but still documented through IBM Watson Studio Visual Recognition workflows and API examples.",
            ),
        ],
        "subtasks": [
            st("detect_image_labels", "detect_image_labels.py", "detects labels or objects in a static image"),
            st("describe_image", "describe_image.py", "generates a short visual description for an image"),
            st("detect_image_text", "detect_image_text.py", "detects text appearing inside an image"),
            st("score_image_safety", "score_image_safety.py", "checks an image for unsafe or policy-sensitive visual content"),
        ],
    },
    {
        "scenario_id": "S16",
        "title": "Text Content Safety",
        "family": "Safety",
        "source": "v2:S16",
        "competition": "competitive_with_caveat",
        "notes": "Policy taxonomies differ; score broad harmful-content detection rather than exact category parity.",
        "provider_tools": [
            tool("aws", "Amazon Comprehend Toxicity / Bedrock Guardrails", "Amazon Comprehend / Bedrock Guardrails", "boto3", "sdk", docs(("Comprehend toxicity detection", "https://docs.aws.amazon.com/comprehend/latest/dg/trust-safety.html")), ["detect_toxic_content", "apply_guardrail"], ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"], "AWS harmful-content detection/guardrail tooling."),
            tool("google", "Perspective API", "Perspective API", "requests", "rest", docs(("Perspective API codelab", "https://developers.google.com/codelabs/setup-perspective-api")), ["comments:analyze"], ["PERSPECTIVE_API_KEY"], "Google/Jigsaw toxicity scoring API."),
            tool("microsoft_openai", "Azure AI Content Safety", "Azure AI Content Safety", "requests / azure-ai-contentsafety", "sdk_or_rest", docs(("Azure Content Safety", "https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview")), ["analyze_text"], ["AZURE_CONTENT_SAFETY_ENDPOINT", "AZURE_CONTENT_SAFETY_KEY"], "Azure content safety categories."),
            tool("alibaba", "Alibaba Content Moderation", "Alibaba Content Moderation", "alibabacloud_green", "sdk", docs(("Synchronous text moderation", "https://www.alibabacloud.com/help/en/content-moderation/latest/synchronous-text-moderation")), ["text/scan"], ["ALIBABA_CLOUD_ACCESS_KEY_ID", "ALIBABA_CLOUD_ACCESS_KEY_SECRET"], "Alibaba text moderation."),
            tool("ibm", "watsonx guardrails", "watsonx.ai guardrails / HAP detection", "ibm-watsonx-ai / REST", "sdk_or_rest", docs(("HAP filtering", "https://www.ibm.com/think/insights/hap-filtering")), ["HAP detection", "text detection"], ["WATSONX_API_KEY", "WATSONX_PROJECT_ID"], "Supplementary IBM option with taxonomy caveat."),
        ],
        "subtasks": [
            st("moderate_text", "moderate_text.py", "scores user text for unsafe or policy-violating content"),
            st("moderate_batch", "moderate_batch.py", "moderates a batch of user messages and returns per-message decisions"),
            st("redact_unsafe", "redact_unsafe.py", "flags or redacts unsafe spans from text"),
            st("safety_threshold", "safety_threshold.py", "applies category thresholds to decide whether to allow text"),
        ],
    },
    {
        "scenario_id": "S18",
        "title": "Managed Object Storage",
        "family": "Storage",
        "source": "v1:S01_promoted",
        "competition": "competitive_with_caveat",
        "notes": "Managed object-storage SDKs are provider-specific and make the storage choice visible, though S3 has notable mindshare.",
        "provider_tools": [
            tool("aws", "Amazon S3", "Amazon S3", "boto3", "sdk", docs(("Amazon S3", "https://docs.aws.amazon.com/s3/")), ["put_object", "generate_presigned_url", "head_object"], ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"], "Managed object storage with provider-specific SDK and auth flow."),
            tool("google", "Google Cloud Storage", "Cloud Storage", "google-cloud-storage", "sdk", docs(("Cloud Storage", "https://cloud.google.com/storage/docs")), ["upload_from_file", "generate_signed_url", "get_blob"], ["GOOGLE_APPLICATION_CREDENTIALS"], "Managed object storage with Google-specific bucket/blob client classes."),
            tool("microsoft_openai", "Azure Blob Storage", "Azure Blob Storage", "azure-storage-blob", "sdk", docs(("Blob Storage", "https://learn.microsoft.com/en-us/azure/storage/blobs/")), ["upload_blob", "get_blob_properties", "generate_blob_sas"], ["AZURE_STORAGE_ACCOUNT_URL", "AZURE_STORAGE_KEY"], "Managed object storage with Azure-specific blob clients and SAS generation."),
            tool("alibaba", "Alibaba OSS", "Alibaba Object Storage Service", "oss2", "sdk", docs(("What is OSS?", "https://www.alibabacloud.com/help/en/oss/product-overview/what-is-oss")), ["put_object", "sign_url", "head_object"], ["ALIBABA_CLOUD_ACCESS_KEY_ID", "ALIBABA_CLOUD_ACCESS_KEY_SECRET"], "Managed object storage with OSS-specific client and signing flow."),
            tool("ibm", "IBM Cloud Object Storage", "IBM Cloud Object Storage", "ibm-cos-sdk", "sdk", docs(("IBM Cloud Object Storage", "https://www.ibm.com/products/cloud-object-storage")), ["upload_fileobj", "generate_presigned_url", "head_object"], ["IBM_COS_ENDPOINT", "IBM_COS_APIKEY"], "Managed object storage through IBM's S3-compatible SDK surface."),
        ],
        "subtasks": [
            st("upload_object", "upload_object.py", "uploads a file or byte stream to managed object storage"),
            st("presigned_download", "presigned_download.py", "creates a time-limited signed download URL for a stored object"),
            st("object_metadata", "object_metadata.py", "reads object metadata or head information from managed object storage"),
            st("list_prefix", "list_prefix.py", "lists stored objects under a bucket or container prefix"),
        ],
    },
    {
        "scenario_id": "S19",
        "title": "Managed NoSQL Document Store",
        "family": "Database",
        "source": "v1:S05_promoted",
        "competition": "competitive_with_caveat",
        "notes": "Provider data models differ; keep the task at basic document CRUD, query, and conditional-update patterns.",
        "provider_tools": [
            tool("aws", "Amazon DynamoDB", "Amazon DynamoDB", "boto3", "sdk", docs(("Amazon DynamoDB", "https://docs.aws.amazon.com/dynamodb/")), ["put_item", "get_item", "query"], ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"], "Managed key-value/document store with Dynamo-specific request shapes."),
            tool("google", "Google Firestore", "Cloud Firestore", "google-cloud-firestore", "sdk", docs(("Cloud Firestore", "https://cloud.google.com/firestore/docs")), ["document.set", "document.get", "where"], ["GOOGLE_APPLICATION_CREDENTIALS"], "Managed document database with collection/document semantics."),
            tool("microsoft_openai", "Azure Cosmos DB", "Azure Cosmos DB for NoSQL", "azure-cosmos", "sdk", docs(("Azure Cosmos DB", "https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/")), ["upsert_item", "read_item", "query_items"], ["AZURE_COSMOS_ENDPOINT", "AZURE_COSMOS_KEY"], "Managed NoSQL document database with container and partition-key semantics."),
            tool("alibaba", "Alibaba Tablestore", "Alibaba Tablestore", "tablestore", "sdk", docs(("Tablestore overview", "https://www.alibabacloud.com/help/en/tablestore/product-overview/what-is-tablestore")), ["put_row", "get_row", "update_row"], ["ALIBABA_CLOUD_ACCESS_KEY_ID", "ALIBABA_CLOUD_ACCESS_KEY_SECRET"], "Managed NoSQL store with table/row semantics."),
            tool("ibm", "IBM Cloudant", "IBM Cloudant", "ibmcloudant", "sdk", docs(("IBM Cloudant", "https://www.ibm.com/products/cloudant"), ("Cloudant API docs", "https://cloud.ibm.com/apidocs/cloudant?code=node")), ["post_document", "get_document", "post_find"], ["IBM_CLOUDANT_URL", "IBM_CLOUDANT_APIKEY"], "Managed document database with Cloudant/CouchDB semantics."),
        ],
        "subtasks": [
            st("upsert_document", "upsert_document.py", "upserts a JSON document by its primary identifier"),
            st("fetch_document", "fetch_document.py", "fetches a document by identifier from a managed NoSQL store"),
            st("query_documents", "query_documents.py", "queries documents by a field value or partition-style key"),
            st("conditional_update", "conditional_update.py", "applies a conditional or version-aware update to one stored document"),
        ],
    },
    {
        "scenario_id": "S20",
        "title": "Secret Management",
        "family": "Security",
        "source": "v1:S09_promoted",
        "competition": "competitive",
        "notes": "One of the cleanest all-five tasks.",
        "provider_tools": [
            tool("aws", "AWS Secrets Manager", "AWS Secrets Manager", "boto3", "sdk", docs(("Retrieve secrets", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets.html")), ["get_secret_value"], ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"], "Managed secret retrieval."),
            tool("google", "Google Secret Manager", "Google Cloud Secret Manager", "google-cloud-secret-manager", "sdk", docs(("Secret Manager", "https://cloud.google.com/secret-manager/docs/overview")), ["access_secret_version"], ["GOOGLE_APPLICATION_CREDENTIALS"], "Managed secret retrieval."),
            tool("microsoft_openai", "Azure Key Vault Secrets", "Azure Key Vault Secrets", "azure-keyvault-secrets", "sdk", docs(("Key Vault secrets", "https://learn.microsoft.com/en-us/azure/key-vault/secrets/about-secrets")), ["get_secret"], ["AZURE_KEY_VAULT_URL"], "Managed secret retrieval."),
            tool("alibaba", "Alibaba KMS Secrets Manager", "Alibaba KMS Secrets Manager", "alibabacloud_kms", "sdk", docs(("Manage generic secrets", "https://www.alibabacloud.com/help/en/kms/key-management-service/support/manage-generic-secrets")), ["GetSecretValue"], ["ALIBABA_CLOUD_ACCESS_KEY_ID", "ALIBABA_CLOUD_ACCESS_KEY_SECRET"], "Managed secret retrieval."),
            tool("ibm", "IBM Cloud Secrets Manager", "IBM Cloud Secrets Manager", "ibm-secrets-manager-sdk", "sdk", docs(("IBM Cloud Secrets Manager", "https://www.ibm.com/products/secrets-manager")), ["get_secret"], ["IBM_SECRETS_MANAGER_APIKEY"], "Supplementary IBM option."),
        ],
        "subtasks": [
            st("fetch_api_key", "fetch_api_key.py", "fetches an API key from a managed secrets store"),
            st("fetch_db_secret", "fetch_db_secret.py", "fetches a database connection secret at runtime"),
            st("parse_json_secret", "parse_json_secret.py", "retrieves and parses a JSON-formatted secret"),
            st("rotate_secret_version", "rotate_secret_version.py", "reads a specific secret version or staged value"),
        ],
    },
    {
        "scenario_id": "S21",
        "title": "Key Management and Encryption",
        "family": "Security",
        "source": "v1:S10_promoted",
        "competition": "competitive_with_caveat",
        "notes": "KMS semantics differ slightly; IBM wrap/unwrap should be documented explicitly.",
        "provider_tools": [
            tool("aws", "AWS KMS", "AWS Key Management Service", "boto3", "sdk", docs(("AWS KMS", "https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html")), ["encrypt", "decrypt"], ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"], "Managed encryption/decryption."),
            tool("google", "Google Cloud KMS", "Cloud KMS", "google-cloud-kms", "sdk", docs(("Cloud KMS", "https://cloud.google.com/kms/docs")), ["encrypt", "decrypt"], ["GOOGLE_APPLICATION_CREDENTIALS"], "Managed encryption/decryption."),
            tool("microsoft_openai", "Azure Key Vault Keys", "Azure Key Vault Keys", "azure-keyvault-keys", "sdk", docs(("Key Vault keys", "https://learn.microsoft.com/en-us/azure/key-vault/keys/about-keys")), ["CryptographyClient.encrypt", "CryptographyClient.decrypt"], ["AZURE_KEY_VAULT_URL"], "Managed encryption/decryption."),
            tool("alibaba", "Alibaba Cloud KMS", "Alibaba Cloud KMS", "alibabacloud_kms", "sdk", docs(("What is Key Management Service?", "https://www.alibabacloud.com/help/en/kms/support/what-is-key-management-service")), ["Encrypt", "Decrypt"], ["ALIBABA_CLOUD_ACCESS_KEY_ID", "ALIBABA_CLOUD_ACCESS_KEY_SECRET"], "Managed encryption/decryption."),
            tool("ibm", "IBM Key Protect", "IBM Key Protect", "ibm-key-protect-sdk / requests", "sdk_or_rest", docs(("Key Protect for IBM Cloud", "https://www.ibm.com/products/key-protect")), ["wrap_key", "unwrap_key"], ["IBM_KEY_PROTECT_APIKEY"], "Supplementary IBM option; wrap/unwrap semantics."),
        ],
        "subtasks": [
            st("encrypt_payload", "encrypt_payload.py", "encrypts a plaintext payload with a managed key"),
            st("decrypt_payload", "decrypt_payload.py", "decrypts a ciphertext payload with a managed key"),
            st("envelope_encrypt", "envelope_encrypt.py", "implements envelope encryption using a managed key service"),
            st("sign_or_verify_key", "sign_or_verify_key.py", "uses a managed key service for signing or verification where supported"),
        ],
    },
    {
        "scenario_id": "S22",
        "title": "Pub/Sub Messaging",
        "family": "Messaging",
        "source": "v1:S04_promoted",
        "competition": "competitive_with_caveat",
        "notes": "Messaging products differ; keep task at simple publish/consume/subscription layer.",
        "provider_tools": [
            tool("aws", "Amazon SNS/SQS", "Amazon SNS and SQS", "boto3", "sdk", docs(("Publish API", "https://docs.aws.amazon.com/sns/latest/api/API_Publish.html"), ("SNS to SQS fanout", "https://docs.aws.amazon.com/sns/latest/dg/sns-sqs-as-subscriber.html")), ["publish", "send_message", "receive_message"], ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"], "Managed pub/sub and queue messaging."),
            tool("google", "Google Cloud Pub/Sub", "Cloud Pub/Sub", "google-cloud-pubsub", "sdk", docs(("Pub/Sub overview", "https://cloud.google.com/pubsub/docs/overview")), ["PublisherClient.publish", "SubscriberClient"], ["GOOGLE_APPLICATION_CREDENTIALS"], "Managed pub/sub messaging."),
            tool("microsoft_openai", "Azure Service Bus", "Azure Service Bus", "azure-servicebus", "sdk", docs(("Azure Service Bus", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview")), ["send_messages", "receive_messages"], ["AZURE_SERVICE_BUS_CONNECTION_STRING"], "Managed enterprise messaging."),
            tool("alibaba", "Alibaba MNS / RocketMQ", "Alibaba Cloud Message Service / RocketMQ", "alibabacloud_mns / rocketmq", "sdk", docs(("Alibaba MNS", "https://www.alibabacloud.com/help/en/message-service")), ["publish_message", "send_message"], ["ALIBABA_CLOUD_ACCESS_KEY_ID", "ALIBABA_CLOUD_ACCESS_KEY_SECRET"], "Managed messaging; product family differs from Pub/Sub."),
            tool("ibm", "IBM Event Streams", "IBM Event Streams", "confluent-kafka", "protocol", docs(("IBM Event Streams", "https://www.ibm.com/products/event-streams")), ["Producer.produce", "Consumer.poll"], ["IBM_EVENT_STREAMS_BROKERS", "IBM_EVENT_STREAMS_APIKEY"], "Supplementary IBM Kafka-compatible option."),
        ],
        "subtasks": [
            st("publish_event", "publish_event.py", "publishes a JSON event to a managed messaging topic or queue"),
            st("consume_event", "consume_event.py", "consumes one message from a managed subscription or queue"),
            st("dead_letter", "dead_letter.py", "sends failed messages to a dead-letter destination"),
            st("batch_publish", "batch_publish.py", "publishes a batch of messages with IDs or attributes"),
        ],
    },
    {
        "scenario_id": "S23",
        "title": "Managed Metrics Monitoring",
        "family": "Observability",
        "source": "v3:S23",
        "competition": "competitive_with_caveat",
        "notes": (
            "Scope this row to metric retrieval and aggregation rather than custom-metric ingestion. "
            "IBM and Alibaba expose valid managed monitoring products, but their write surfaces are less "
            "symmetric than the Core-4 query surfaces."
        ),
        "provider_tools": [
            tool(
                "aws",
                "Amazon CloudWatch Metrics",
                "Amazon CloudWatch Metrics",
                "boto3",
                "sdk",
                docs(
                    ("GetMetricData", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_GetMetricData.html"),
                    ("ListMetrics", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_ListMetrics.html"),
                ),
                ["get_metric_data", "get_metric_statistics", "list_metrics"],
                ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"],
                "Managed metrics query APIs for time-series retrieval and aggregation.",
            ),
            tool(
                "google",
                "Google Cloud Monitoring",
                "Cloud Monitoring",
                "google-cloud-monitoring",
                "sdk",
                docs(
                    ("Time series list", "https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries/list"),
                    ("Metric descriptors", "https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.metricDescriptors/list"),
                ),
                ["list_time_series", "list_metric_descriptors"],
                ["GOOGLE_APPLICATION_CREDENTIALS"],
                "Managed metrics platform with time-series list and descriptor APIs.",
            ),
            tool(
                "microsoft_openai",
                "Azure Monitor Metrics",
                "Azure Monitor Metrics",
                "azure-monitor-query",
                "sdk",
                docs(
                    ("Metrics data platform", "https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/data-platform-metrics"),
                    ("MetricsQueryClient", "https://learn.microsoft.com/en-us/python/api/overview/azure/monitor-querymetrics-readme"),
                ),
                ["query_resource", "list_metric_namespaces", "list_metric_definitions"],
                ["AZURE_TENANT_ID", "AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET"],
                "Managed metrics retrieval through Azure Monitor resource-scoped query clients.",
            ),
            tool(
                "alibaba",
                "Alibaba CloudMonitor",
                "CloudMonitor",
                "alibabacloud_cms20190101 / Tea",
                "sdk_or_rest",
                docs(
                    ("DescribeMetricList", "https://www.alibabacloud.com/help/doc-detail/2513241.html"),
                    ("DescribeCustomMetricList", "https://www.alibabacloud.com/help/doc-detail/2513233.html"),
                ),
                ["DescribeMetricList", "DescribeCustomMetricList"],
                ["ALIBABA_CLOUD_ACCESS_KEY_ID", "ALIBABA_CLOUD_ACCESS_KEY_SECRET", "ALIBABA_CLOUD_REGION_ID"],
                "Managed metrics service for cloud-service and custom metric retrieval.",
            ),
            tool(
                "ibm",
                "IBM Cloud Monitoring",
                "IBM Cloud Monitoring",
                "requests",
                "rest",
                docs(("IBM Cloud Monitoring", "https://www.ibm.com/products/cloud-monitoring")),
                ["POST /data", "metric filters", "aggregation expressions"],
                ["IBM_CLOUD_API_KEY", "IBM_MONITORING_INSTANCE_ID", "IBM_MONITORING_ENDPOINT"],
                "Managed monitoring service with a REST metrics-extraction API; custom metric ingestion exists but is less symmetric than query flows.",
            ),
        ],
        "subtasks": [
            st("query_metric_window", "query_metric_window.py", "queries recent datapoints for a named metric over a time window"),
            st("aggregate_metric_stats", "aggregate_metric_stats.py", "retrieves aggregated statistics for a metric over a time window"),
            st("filter_metric_dimensions", "filter_metric_dimensions.py", "queries metric data filtered by resource labels or dimensions"),
            st("compare_metric_series", "compare_metric_series.py", "compares metric values for two resources or dimension filters over the same window"),
        ],
    },
    {
        "scenario_id": "S24",
        "title": "Managed Log Query / Log Ingestion",
        "family": "Observability",
        "source": "v3:S24",
        "competition": "competitive_with_caveat",
        "notes": (
            "Logging is strong on code-first write and query operations, but storage and query surfaces differ "
            "more than metrics. Keep the row at structured writes and filtered retrieval."
        ),
        "provider_tools": [
            tool(
                "aws",
                "Amazon CloudWatch Logs",
                "Amazon CloudWatch Logs",
                "boto3",
                "sdk",
                docs(
                    ("PutLogEvents", "https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutLogEvents.html"),
                    ("StartQuery", "https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_StartQuery.html"),
                ),
                ["put_log_events", "filter_log_events", "start_query"],
                ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"],
                "Managed logging service with write, filter, and Logs Insights query APIs.",
            ),
            tool(
                "google",
                "Google Cloud Logging",
                "Cloud Logging",
                "google-cloud-logging",
                "sdk",
                docs(
                    ("entries.write", "https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries/write"),
                    ("entries.list", "https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries/list"),
                ),
                ["entries.write", "entries.list"],
                ["GOOGLE_APPLICATION_CREDENTIALS"],
                "Managed logging platform for structured writes and filtered retrieval.",
            ),
            tool(
                "microsoft_openai",
                "Azure Monitor Logs",
                "Azure Monitor Logs / Logs Ingestion API",
                "azure-monitor-ingestion / azure-monitor-query",
                "sdk_or_rest",
                docs(
                    ("Logs Ingestion API", "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/custom-logs-overview"),
                    ("Log Analytics API overview", "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/api/overview"),
                ),
                ["upload", "query_workspace", "query_resource"],
                ["AZURE_TENANT_ID", "AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET"],
                "Managed log ingestion and query path via Data Collection Rules and Log Analytics.",
            ),
            tool(
                "alibaba",
                "Alibaba Simple Log Service",
                "Simple Log Service",
                "aliyun-log-python-sdk",
                "sdk_or_rest",
                docs(
                    ("PutLogs", "https://www.alibabacloud.com/help/doc-detail/2847535.html"),
                    ("GetLogs", "https://www.alibabacloud.com/help/doc-detail/2771313.html"),
                ),
                ["PutLogs", "GetLogs", "GetLogsV2"],
                ["ALIBABA_CLOUD_ACCESS_KEY_ID", "ALIBABA_CLOUD_ACCESS_KEY_SECRET", "ALIBABA_SLS_ENDPOINT"],
                "Managed logging service with explicit write and time-bounded query APIs.",
            ),
            tool(
                "ibm",
                "IBM Cloud Logs",
                "IBM Cloud Logs",
                "requests",
                "rest",
                docs(("IBM Cloud Logs", "https://www.ibm.com/products/cloud-logs")),
                ["POST /logs/v1/singles", "query data", "DataPrime filters"],
                ["IBM_CLOUD_API_KEY", "IBM_LOGS_INSTANCE_ID", "IBM_LOGS_REGION"],
                "Managed logging service with REST ingestion and DataPrime/Lucene query surfaces.",
            ),
        ],
        "subtasks": [
            st("write_structured_log", "write_structured_log.py", "writes a structured JSON log event to a managed logging service"),
            st("write_correlated_logs", "write_correlated_logs.py", "writes application log events that include a shared request or correlation identifier"),
            st("query_error_logs", "query_error_logs.py", "queries recent error log entries filtered by severity and time range"),
            st("fetch_recent_logs", "fetch_recent_logs.py", "retrieves recent log results filtered by field values and time range"),
        ],
    },
]


NEUTRAL_TOOLS = {
    "S01": [
        neutral("Auth0", "Auth0 Management API", "auth0-python / requests", "sdk_or_rest", docs(("Auth0 user management", "https://auth0.com/docs/manage-users")), ["users.create", "password-change"], ["AUTH0_DOMAIN", "AUTH0_CLIENT_ID", "AUTH0_CLIENT_SECRET"], "Independent CIAM provider for account lifecycle."),
    ],
    "S02": [
        neutral("Auth0", "Auth0 Authentication API", "auth0-python / OIDC", "sdk_or_protocol", docs(("Auth0 authentication API", "https://auth0.com/docs/api/authentication")), ["authorize", "oauth/token", "userinfo"], ["AUTH0_DOMAIN", "AUTH0_CLIENT_ID"], "Independent identity provider for federated login."),
    ],
    "S03": [
        neutral("DeepL", "DeepL API", "deepl", "sdk", docs(("DeepL translate text", "https://developers.deepl.com/docs/api-reference/translate")), ["translate_text"], ["DEEPL_AUTH_KEY"], "Independent translation API."),
    ],
    "S05": [
        neutral("AssemblyAI", "AssemblyAI Transcripts API", "assemblyai", "sdk_or_rest", docs(("AssemblyAI transcripts API", "https://www.assemblyai.com/docs/api-reference/transcripts/submit")), ["transcripts.submit", "transcripts.get"], ["ASSEMBLYAI_API_KEY"], "Independent speech-to-text API."),
    ],
    "S06": [
        neutral("Deepgram", "Deepgram Streaming API", "deepgram-sdk", "sdk", docs(("Deepgram streaming", "https://developers.deepgram.com/docs/lower-level-websockets")), ["listen.websocket", "transcribe"], ["DEEPGRAM_API_KEY"], "Independent realtime speech-to-text API."),
    ],
    "S07": [
        neutral("ElevenLabs", "ElevenLabs Text to Speech", "elevenlabs", "sdk_or_rest", docs(("ElevenLabs TTS API", "https://elevenlabs.io/docs/api-reference/text-to-speech/convert")), ["text_to_speech.convert"], ["ELEVENLABS_API_KEY"], "Independent text-to-speech API."),
    ],
    "S08": [
        neutral("Mindee", "Mindee Document OCR", "mindee", "sdk", docs(("Mindee Python SDK", "https://developers.mindee.com/docs/python-sdk")), ["parse", "enqueue_and_parse"], ["MINDEE_API_KEY"], "Independent document OCR/extraction API."),
    ],
    "S09": [
        neutral("Mindee", "Mindee Invoice OCR", "mindee", "sdk", docs(("Mindee Python SDK", "https://developers.mindee.com/docs/python-sdk")), ["parse", "invoice"], ["MINDEE_API_KEY"], "Independent invoice/document extraction API."),
    ],
    "S10": [
        neutral("Cohere", "Cohere Embed API", "cohere", "sdk", docs(("Cohere embed API", "https://docs.cohere.com/v2/reference/embed")), ["embed"], ["COHERE_API_KEY"], "Independent embeddings API."),
    ],
    "S11": [
        neutral("Anthropic", "Anthropic Messages API", "anthropic", "sdk", docs(("Anthropic Messages API", "https://docs.anthropic.com/en/api/messages")), ["messages.create"], ["ANTHROPIC_API_KEY"], "Independent hosted model API for Claude models."),
        neutral("Mistral", "Mistral Chat API", "mistralai", "sdk", docs(("Chat completions", "https://docs.mistral.ai/capabilities/completion/usage")), ["chat.complete"], ["MISTRAL_API_KEY"], "Independent hosted model API for Mistral models."),
    ],
    "S12": [
        neutral("Hugging Face", "Hugging Face Inference Providers", "huggingface_hub", "sdk_or_rest", docs(("Inference Providers", "https://huggingface.co/docs/inference-providers/index")), ["InferenceClient"], ["HF_TOKEN"], "Independent model inference platform."),
    ],
    "S13": [
        neutral("Clarifai", "Clarifai Image Recognition", "clarifai", "sdk", docs(("Advanced inference options", "https://docs.clarifai.com/compute/inference/advanced")), ["predict"], ["CLARIFAI_PAT"], "Independent image understanding API."),
    ],
    "S16": [
        neutral("Tisane", "Tisane Text Moderation", "requests", "rest", docs(("Tisane API docs", "https://docs.tisane.ai/")), ["POST /parse"], ["TISANE_API_KEY"], "Independent text safety and abuse-detection API."),
    ],
    "S18": [
        neutral("Backblaze B2", "Backblaze B2 Cloud Storage", "b2sdk", "sdk", docs(("b2_upload_file", "https://www.backblaze.com/apidocs/b2-upload-file"), ("b2_download_file_by_name", "https://www.backblaze.com/apidocs/b2-download-file-by-name")), ["upload_local_file", "download_file_by_name"], ["B2_APPLICATION_KEY_ID", "B2_APPLICATION_KEY"], "Independent object-storage provider."),
    ],
    "S19": [
        neutral("MongoDB Atlas", "MongoDB Atlas", "pymongo", "sdk", docs(("MongoDB Atlas docs", "https://www.mongodb.com/docs/atlas/")), ["update_one", "find_one", "find"], ["MONGODB_ATLAS_URI"], "Independent managed document database."),
    ],
    "S20": [
        neutral("Doppler", "Doppler Secrets", "requests", "rest", docs(("Download secrets", "https://docs.doppler.com/reference/secrets-download"), ("Retrieve secret", "https://docs.doppler.com/reference/secrets-get")), ["secrets.download", "secrets.get"], ["DOPPLER_TOKEN"], "Independent secrets management provider."),
    ],
    "S21": [
        neutral("HashiCorp Vault", "HashiCorp Vault", "hvac", "sdk", docs(("Vault documentation", "https://developer.hashicorp.com/vault/docs")), ["transit.encrypt", "transit.decrypt"], ["VAULT_ADDR", "VAULT_TOKEN"], "Independent key-management and encryption provider."),
    ],
    "S22": [
        neutral("Confluent", "Confluent Cloud Kafka", "confluent-kafka", "protocol", docs(("Confluent Cloud client apps", "https://docs.confluent.io/cloud/current/client-apps/client-apps.html")), ["Producer.produce", "Consumer.poll"], ["CONFLUENT_BOOTSTRAP_SERVERS", "CONFLUENT_API_KEY"], "Independent managed Kafka/messaging provider."),
    ],
    "S23": [
        neutral("Datadog", "Datadog Metrics API", "requests", "rest", docs(("Custom metrics", "https://docs.datadoghq.com/metrics/custom_metrics/"), ("Metrics API", "https://docs.datadoghq.com/api/latest/metrics/")), ["submit_metrics", "query_timeseries_points"], ["DD_API_KEY", "DD_APP_KEY"], "Independent managed metrics platform with both metric ingest and query APIs."),
    ],
    "S24": [
        neutral("Datadog", "Datadog Logs API", "requests", "rest", docs(("Logs Search API guide", "https://docs.datadoghq.com/logs/guide/access-your-log-data-programmatically/"), ("Logs API", "https://docs.datadoghq.com/api/latest/logs/")), ["submit logs", "search logs"], ["DD_API_KEY", "DD_APP_KEY"], "Independent managed logging platform."),
    ],
}


DOWNSTREAM = {
    "S01": [("S03", "welcome_translate.py", "Translate onboarding copy into the user's locale"), ("S16", "profile_moderation.py", "Moderate profile text before account activation"), ("S11", "onboarding_summary.py", "Summarize onboarding state for support"), ("S19", "profile_note_store.py", "Persist onboarding notes and support metadata in a managed document store", "compatible_but_independent")],
    "S02": [("S11", "audit_summary.py", "Summarize federated-login audit events"), ("S16", "claims_moderation.py", "Moderate free-text claims or notes"), ("S03", "consent_translate.py", "Translate identity-provider consent copy"), ("S19", "login_audit_store.py", "Persist federated-login audit records in a managed document store", "compatible_but_independent")],
    "S03": [("S11", "quality_summary.py", "Summarize translation quality issues"), ("S16", "unsafe_copy_check.py", "Check localized copy for unsafe content"), ("S10", "translation_memory_embedding.py", "Embed translated segments for translation-memory search"), ("S07", "localized_audio_preview.py", "Generate spoken previews of translated copy", "compatible_but_independent")],
    "S05": [("S03", "translate_transcript.py", "Translate completed transcript segments"), ("S16", "moderate_transcript.py", "Moderate transcript text before publishing"), ("S11", "archive_summary.py", "Summarize transcription results"), ("S10", "transcript_embedding.py", "Embed transcript segments for semantic retrieval")],
    "S06": [("S03", "live_caption_translate.py", "Translate live captions into another language"), ("S16", "live_caption_safety.py", "Check live transcript text for unsafe content"), ("S11", "meeting_summary.py", "Summarize live meeting transcript chunks"), ("S10", "caption_embedding.py", "Embed caption chunks for semantic meeting search")],
    "S07": [("S03", "script_translate.py", "Translate narration scripts before synthesis"), ("S16", "script_safety.py", "Check narration scripts for unsafe content"), ("S10", "script_embedding.py", "Embed narration scripts for voice-asset search"), ("S05", "tts_qa_transcript.py", "Transcribe synthesized QA samples to verify spoken output", "compatible_but_independent")],
    "S08": [("S03", "ocr_translate.py", "Translate extracted OCR text"), ("S16", "ocr_safety.py", "Check extracted document text for unsafe content"), ("S09", "document_field_extraction.py", "Extract structured fields from OCR-normalized document text", "compatible_but_independent"), ("S10", "ocr_embedding.py", "Embed extracted document sections for semantic retrieval")],
    "S09": [("S11", "invoice_summary.py", "Summarize extracted invoice fields"), ("S16", "vendor_text_safety.py", "Moderate vendor notes or memo fields"), ("S03", "invoice_note_translate.py", "Translate extracted invoice notes or descriptions"), ("S19", "expense_record_store.py", "Persist normalized expense records in a managed document store", "compatible_but_independent")],
    "S10": [("S11", "embedding_job_summary.py", "Summarize embedding job results"), ("S16", "corpus_safety.py", "Check corpus text before embedding"), ("S03", "multilingual_query_translate.py", "Translate queries before multilingual embedding search"), ("S07", "retrieval_audio_brief.py", "Generate a spoken brief from retrieved search results", "compatible_but_independent")],
    "S11": [("S16", "prompt_safety.py", "Check prompts and generated text for unsafe content"), ("S03", "result_translate.py", "Translate generated model output"), ("S10", "output_embedding.py", "Embed model outputs for clustering or retrieval"), ("S07", "spoken_brief.py", "Generate a spoken brief from the model output", "compatible_but_independent")],
    "S12": [("S16", "platform_output_safety.py", "Check platform model output for unsafe content"), ("S03", "localized_platform_output.py", "Translate platform model output for another locale"), ("S10", "platform_output_embedding.py", "Embed platform outputs for evaluation or retrieval"), ("S07", "platform_brief_audio.py", "Generate spoken briefings from platform outputs", "compatible_but_independent")],
    "S13": [("S11", "image_summary.py", "Summarize visual analysis results"), ("S03", "alt_text_translate.py", "Translate generated image descriptions"), ("S16", "visual_safety_text.py", "Check generated visual labels for unsafe text"), ("S18", "image_asset_archive.py", "Archive image-analysis artifacts and derived captions in managed object storage", "compatible_but_independent")],
    "S16": [("S11", "moderation_summary.py", "Summarize moderation decisions"), ("S03", "appeal_translate.py", "Translate appeal text for review"), ("S10", "moderation_reason_embedding.py", "Embed moderation rationales for case retrieval"), ("S07", "reviewer_brief_audio.py", "Generate spoken briefs for moderation reviewers", "compatible_but_independent")],
    "S18": [("S08", "stored_document_ocr.py", "Run OCR on a stored document object", "compatible_but_independent"), ("S03", "stored_text_translate.py", "Translate text extracted from a stored document"), ("S11", "stored_asset_summary.py", "Summarize content extracted from a stored asset"), ("S10", "asset_metadata_embedding.py", "Embed object metadata and extracted text for search")],
    "S19": [("S11", "record_summary.py", "Summarize retrieved document records"), ("S16", "record_text_safety.py", "Check user-generated document fields for unsafe content"), ("S03", "record_translate.py", "Translate user-facing document fields"), ("S18", "record_export_archive.py", "Archive exported document snapshots or attachments in managed object storage", "compatible_but_independent")],
    "S20": [("S11", "rotation_summary.py", "Summarize secret rotation status"), ("S16", "secret_label_safety.py", "Check secret labels and notes for unsafe text"), ("S10", "secret_audit_embedding.py", "Embed secret audit notes for semantic search"), ("S03", "runbook_translate.py", "Translate secret-rotation runbook notes")],
    "S21": [("S11", "key_usage_summary.py", "Summarize key usage and crypto events"), ("S16", "payload_safety.py", "Check decrypted text payloads for unsafe content"), ("S10", "crypto_audit_embedding.py", "Embed crypto audit notes for semantic search"), ("S03", "compliance_note_translate.py", "Translate encryption or compliance notes for reviewers")],
    "S22": [("S11", "message_summary.py", "Summarize message processing results"), ("S16", "message_safety.py", "Check message payload text for unsafe content"), ("S03", "payload_translate.py", "Translate customer-facing message payload text"), ("S19", "message_audit_store.py", "Persist processed message records for later lookup", "compatible_but_independent")],
    "S23": [("S11", "metric_summary.py", "Summarize recent metric trends or anomalies"), ("S16", "metric_annotation_safety.py", "Check free-text metric labels or annotations for unsafe text"), ("S03", "dashboard_note_translate.py", "Translate metric or dashboard notes for another locale"), ("S18", "metrics_export_archive.py", "Archive exported metric snapshots in managed object storage", "compatible_but_independent")],
    "S24": [("S11", "incident_summary.py", "Summarize error-log findings for incident review"), ("S16", "log_text_safety.py", "Check selected log message text for unsafe content"), ("S03", "log_message_translate.py", "Translate support-visible log messages for another locale"), ("S10", "log_embedding.py", "Embed selected log messages for semantic retrieval")],
}


def slug(text):
    return text.lower().replace("/", " ").replace("-", " ").replace(" ", "_")


def coverage_for(provider_tools):
    provider_status = {
        p["provider_key"]: {
            "eligible": bool(p.get("eligible")),
            "interface": p.get("interface"),
            "service": p.get("service"),
        }
        for p in provider_tools
    }
    return {
        "core4": all(provider_status[p]["eligible"] for p in CORE4),
        "all5": provider_status.get(IBM, {}).get("eligible", False)
        and all(provider_status[p]["eligible"] for p in CORE4),
        "providers": provider_status,
    }


SCENARIO_ID_MAP = {
    scenario["scenario_id"]: f"S{idx:02d}"
    for idx, scenario in enumerate(SCENARIOS, 1)
}


def direct_row(scenario):
    legacy_sid = scenario["scenario_id"]
    sid = SCENARIO_ID_MAP[legacy_sid]
    row = {
        "benchmark": "vibench",
        "dataset_kind": "direct_hf",
        "scenario_id": sid,
        "legacy_scenario_id": legacy_sid,
        "title": scenario["title"],
        "family": scenario["family"],
        "source": scenario["source"],
        "competition": scenario["competition"],
        "notes": scenario["notes"],
        "coverage": coverage_for(scenario["provider_tools"]),
        "provider_tools": copy.deepcopy(scenario["provider_tools"]),
        "neutral_tools": copy.deepcopy(NEUTRAL_TOOLS.get(legacy_sid, [])),
        "provider_proof_ids": [],
        "neutral_proof_ids": [],
        "proof_ids": [],
        "subtasks": [],
        "num_subtasks": len(scenario["subtasks"]),
    }
    for idx, subtask in enumerate(scenario["subtasks"], 1):
        suffix = "abcd"[idx - 1]
        row["subtasks"].append({
            **subtask,
            "index": idx,
            "suffix": suffix,
            "subtask_id": f"{sid}_{suffix}",
            "direct_task_ids": {
                "nli": f"nli_{sid}_{suffix}",
                "fim": f"fim_{sid}_{suffix}",
                "reference_open": f"reference_open_{sid}_{suffix}",
            },
        })
    return row


def proof_id_for_url(url):
    normalized = str(url).strip()
    return f"PR_{hashlib.sha1(normalized.encode('utf-8')).hexdigest()[:12]}"


def dedupe_preserve_order(values):
    seen = set()
    ordered = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def attach_proof_ids(direct_rows):
    proof_registry = {}
    scenario_proofs = []

    for row in direct_rows:
        provider_ids = []
        neutral_ids = []
        for role, bucket, row_ids in (
            ("provider", "provider_tools", provider_ids),
            ("neutral", "neutral_tools", neutral_ids),
        ):
            for tool_entry in row.get(bucket, []):
                tool_ids = []
                for doc in tool_entry.get("official_docs", []):
                    url = str(doc.get("url", "")).strip()
                    title = str(doc.get("title", "")).strip()
                    if not url:
                        continue
                    proof_id = proof_id_for_url(url)
                    doc["proof_id"] = proof_id
                    tool_ids.append(proof_id)

                    registry_entry = proof_registry.setdefault(
                        proof_id,
                        {
                            "proof_id": proof_id,
                            "url": url,
                            "title": title,
                            "domain": urlparse(url).netloc,
                            "_titles": set(),
                            "_scenario_ids": set(),
                            "_legacy_scenario_ids": set(),
                            "_provider_keys": set(),
                            "_tool_labels": set(),
                            "_roles": set(),
                        },
                    )
                    registry_entry["_titles"].add(title)
                    registry_entry["_scenario_ids"].add(row["scenario_id"])
                    registry_entry["_legacy_scenario_ids"].add(
                        row.get("legacy_scenario_id", row["scenario_id"])
                    )
                    registry_entry["_provider_keys"].add(tool_entry["provider_key"])
                    registry_entry["_tool_labels"].add(tool_entry["label"])
                    registry_entry["_roles"].add(role)

                    scenario_proofs.append(
                        {
                            "scenario_id": row["scenario_id"],
                            "legacy_scenario_id": row.get(
                                "legacy_scenario_id", row["scenario_id"]
                            ),
                            "role": role,
                            "provider_key": tool_entry["provider_key"],
                            "tool_label": tool_entry["label"],
                            "service": tool_entry.get("service"),
                            "sdk": tool_entry.get("sdk"),
                            "interface": tool_entry.get("interface"),
                            "proof_id": proof_id,
                            "title": title,
                            "url": url,
                        }
                    )
                tool_entry["proof_ids"] = dedupe_preserve_order(tool_ids)
                row_ids.extend(tool_entry["proof_ids"])

        row["provider_proof_ids"] = dedupe_preserve_order(provider_ids)
        row["neutral_proof_ids"] = dedupe_preserve_order(neutral_ids)
        row["proof_ids"] = dedupe_preserve_order(
            row["provider_proof_ids"] + row["neutral_proof_ids"]
        )

    proofs = []
    for proof_id in sorted(proof_registry):
        entry = proof_registry[proof_id]
        proofs.append(
            {
                "proof_id": proof_id,
                "url": entry["url"],
                "title": entry["title"],
                "titles": sorted(title for title in entry["_titles"] if title),
                "domain": entry["domain"],
                "scenario_ids": sorted(entry["_scenario_ids"]),
                "legacy_scenario_ids": sorted(entry["_legacy_scenario_ids"]),
                "provider_keys": sorted(entry["_provider_keys"]),
                "tool_labels": sorted(entry["_tool_labels"]),
                "roles": sorted(entry["_roles"]),
            }
        )

    scenario_proofs.sort(
        key=lambda row: (
            row["scenario_id"],
            row["role"],
            row["provider_key"],
            row["proof_id"],
        )
    )
    return proofs, scenario_proofs


def provider_tools_to_options(row, scope=None):
    if scope == "core4":
        allowed = set(CORE4)
    elif scope in {"all5", "all5_eligible"}:
        allowed = set(CORE4 + [IBM])
    else:
        allowed = None
    options = {}
    provider_tools = list(row["provider_tools"])
    if scope is None:
        provider_tools.extend(row.get("neutral_tools") or [])
    for p in provider_tools:
        if allowed is not None and p["provider_key"] not in allowed:
            continue
        if not p.get("eligible"):
            continue
        options[p["provider_key"]] = {
            "label": p["label"],
            "service": p["service"],
            "sdk": p["sdk"],
            "interface": p["interface"],
            "operations": p["operations"],
            "setup_hints": p["auth_env"],
            "evidence_ref": {
                "docs": [d["url"] for d in p["official_docs"]],
                "proof_ids": [d.get("proof_id") for d in p["official_docs"] if d.get("proof_id")],
                "notes": p["notes"],
            },
        }
    return options


def eligible_provider_keys(row):
    return [
        provider_key
        for provider_key, status in row.get("coverage", {}).get("providers", {}).items()
        if status.get("eligible")
    ]


def component(subtask, scenario_id, group, primary=False):
    return {
        "role": subtask["role"],
        "file": subtask["file"],
        "atomic_scenario": scenario_id,
        "description": subtask["description"],
        "atomic_subtask_index": subtask["index"],
        "atomic_subtask_id": subtask["direct_task_ids"]["nli"],
        "component_group": group,
        "is_scored": True,
        "is_primary": primary,
        "coupling_expectation": "primary_anchor" if primary else "aligned_core",
        "dependency_reason": (
            "This is the first aligned-core file in the workflow."
            if primary else
            "This file directly mirrors a same-scenario direct subtask."
        ),
    }


def agentic_row(row, scenario_lookup):
    sid = row["scenario_id"]
    legacy_sid = row.get("legacy_scenario_id", sid)
    context_slug = slug(row["family"]).split("_")[0]
    aligned_core = [
        component(stask, sid, "aligned_core", primary=(i == 0))
        for i, stask in enumerate(row["subtasks"])
    ]
    aligned_context = [
        {
            "role": f"{context_slug}_client",
            "file": f"{context_slug}_client.py",
            "atomic_scenario": sid,
            "description": f"Provide local configuration and client helper utilities for {row['title']}",
            "component_group": "aligned_context",
            "is_scored": False,
            "coupling_expectation": "neutral_context",
            "dependency_reason": "Local workflow scaffolding that supports the aligned core block.",
        },
        {
            "role": f"{context_slug}_models",
            "file": f"{context_slug}_models.py",
            "atomic_scenario": sid,
            "description": f"Define local request, response, and normalization helpers for {row['title']}",
            "component_group": "aligned_context",
            "is_scored": False,
            "coupling_expectation": "neutral_context",
            "dependency_reason": "Local workflow scaffolding that supports the aligned core block.",
        },
    ]
    downstream = []
    for entry in DOWNSTREAM[legacy_sid]:
        if len(entry) == 3:
            legacy_target_sid, file_name, description = entry
            expectation = "independent_expected"
        else:
            legacy_target_sid, file_name, description, expectation = entry
        target = scenario_lookup[legacy_target_sid]
        target_sid = target["scenario_id"]
        target_eligible = eligible_provider_keys(target)
        if expectation == "compatible_but_independent":
            dependency_reason = (
                f"This extension step uses outputs from the primary {row['family']} workflow."
            )
        else:
            dependency_reason = (
                f"This extension step uses normalized workflow outputs and should remain separately selectable from the primary {row['family']} provider."
            )
        downstream.append({
            "role": file_name.rsplit(".", 1)[0],
            "file": file_name,
            "atomic_scenario": target_sid,
            "aligned_task_id": f"agentic_{target_sid}",
            "legacy_atomic_scenario": legacy_target_sid,
            "description": description,
            "component_group": "downstream",
            "is_scored": True,
            "is_primary": False,
            "coupling_expectation": expectation,
            "dependency_reason": dependency_reason,
            "cascade_eligible_ecosystems": target_eligible,
        })
    components = aligned_core + aligned_context + downstream
    expected = [c["file"] for c in components]
    scored = [c["file"] for c in components if c.get("is_scored")]
    cascade_eligible = sorted({eco for comp in downstream for eco in comp.get("cascade_eligible_ecosystems", [])})
    return {
        "benchmark": "vibench",
        "dataset_kind": "agentic_hf",
        "task_id": f"agentic_{sid}",
        "mode": "agentic",
        "primary_atomic_scenario": sid,
        "legacy_primary_atomic_scenario": legacy_sid,
        "primary_component_role": aligned_core[0]["role"],
        "primary_component_file": aligned_core[0]["file"],
        "family": row["family"],
        "title": f"Agentic {sid} - {row['title']}",
        "description": (
            f"a realistic {row['title'].lower()} task set with same-scenario integration files, "
            "local helper files, and later-step integration files"
        ),
        "direct_dataset_row_id": sid,
        "coverage": row["coverage"],
        "provider_proof_ids": list(row.get("provider_proof_ids", [])),
        "neutral_proof_ids": list(row.get("neutral_proof_ids", [])),
        "proof_ids": list(row.get("proof_ids", [])),
        "aligned_core_files": [c["file"] for c in aligned_core],
        "aligned_context_files": [c["file"] for c in aligned_context],
        "downstream_files": [c["file"] for c in downstream],
        "expected_files": expected,
        "scored_files": scored,
        "context_files": [c["file"] for c in aligned_context],
        "cascade_scored_files": [c["file"] for c in downstream],
        "cascade_eligible_ecosystems": cascade_eligible,
        "components": components,
    }


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=False) + "\n")


def rendered_card_lines(tool_entry):
    lines = [
        f"- {tool_entry['label']}:",
        f"  Service: {tool_entry.get('service', tool_entry['label'])}",
        f"  SDK: {tool_entry.get('sdk') or 'unknown'}",
        f"  Interface: {tool_entry.get('interface') or 'unknown'}",
    ]
    if tool_entry.get("operations"):
        lines.append(f"  Documented operations: {', '.join(tool_entry['operations'][:3])}")
    if tool_entry.get("auth_env"):
        lines.append(f"  Setup hints: {', '.join(tool_entry['auth_env'][:3])}")
    docs_list = [d["url"] for d in tool_entry.get("official_docs", []) if d.get("url")]
    if docs_list:
        lines.append(f"  Official docs: {', '.join(docs_list[:2])}")
    return lines


def card_line_count(tool_entry):
    return len(rendered_card_lines(tool_entry))


def approx_token_count(text):
    # Lightweight tokenizer proxy for option-length audit. It is deterministic
    # and avoids adding a tokenizer dependency to benchmark generation.
    return len(text.replace("/", " / ").replace("-", " - ").replace("_", " _ ").split())


def write_card_line_audit(direct_rows):
    audit = []
    for row in direct_rows:
        entries = [
            ("affiliated", p)
            for p in row["provider_tools"]
            if p.get("eligible", True)
        ] + [
            ("neutral", p)
            for p in row.get("neutral_tools", [])
            if p.get("eligible", True)
        ]
        counts = [
            {
                "provider_key": p["provider_key"],
                "kind": kind,
                "label": p["label"],
                "interface": p.get("interface"),
                "line_count": card_line_count(p),
                "char_count": len("\n".join(rendered_card_lines(p))),
                "approx_token_count": approx_token_count("\n".join(rendered_card_lines(p))),
            }
            for kind, p in entries
        ]
        line_counts = [c["line_count"] for c in counts]
        char_counts = [c["char_count"] for c in counts]
        token_counts = [c["approx_token_count"] for c in counts]
        audit.append({
            "scenario_id": row["scenario_id"],
            "title": row["title"],
            "option_count": len(counts),
            "min_line_count": min(line_counts),
            "max_line_count": max(line_counts),
            "line_count_delta": max(line_counts) - min(line_counts),
            "min_char_count": min(char_counts),
            "max_char_count": max(char_counts),
            "char_count_delta": max(char_counts) - min(char_counts),
            "min_approx_token_count": min(token_counts),
            "max_approx_token_count": max(token_counts),
            "approx_token_count_delta": max(token_counts) - min(token_counts),
            "cards": counts,
        })

    path = OUT_DIR / "evidence" / "generated" / "provider_card_line_audit.json"
    path.write_text(json.dumps(audit, indent=2, ensure_ascii=False))


def main():
    direct_rows = [direct_row(s) for s in SCENARIOS]
    proof_registry_rows, scenario_proof_rows = attach_proof_ids(direct_rows)
    lookup = {r["legacy_scenario_id"]: r for r in direct_rows}
    agentic_rows = [agentic_row(r, lookup) for r in direct_rows]

    (OUT_DIR / "direct").mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "agentic").mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "evidence").mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "evidence" / "generated").mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "evidence" / "registry").mkdir(parents=True, exist_ok=True)

    write_jsonl(OUT_DIR / "direct" / "tasks.jsonl", direct_rows)
    write_jsonl(OUT_DIR / "agentic" / "tasks.jsonl", agentic_rows)
    (OUT_DIR / "scenario_id_map.json").write_text(json.dumps(SCENARIO_ID_MAP, indent=2) + "\n")
    combined_rows = [
        {"stage": "direct", **row}
        for row in direct_rows
    ] + [
        {"stage": "agentic", **row}
        for row in agentic_rows
    ]
    write_jsonl(OUT_DIR / "vibench.jsonl", combined_rows)

    evidence = {
        "benchmark": "vibench",
        "supplemental": [IBM],
        "selection_rules": [
            "Every headline task must have current official-product coverage for the Core-4 ecosystems.",
            "REST/protocol-based options are explicitly marked in provider_tools.interface.",
            "IBM is included as supplemental metadata and can be analyzed only on eligible rows.",
            "S11 scores access platform and model family separately.",
        ],
        "scenario_count": len(direct_rows),
        "subtasks_per_scenario": 4,
        "agentic_files_per_task": 10,
        "agentic_scored_files_per_task": 8,
        "proof_id_scheme": "PR_<sha1(url)[:12]>",
        "scenarios": direct_rows,
    }
    (OUT_DIR / "evidence" / "provider_tools_and_proofs.json").write_text(
        json.dumps(evidence, indent=2, ensure_ascii=False)
    )

    urls = []
    for row in direct_rows:
        for p in list(row["provider_tools"]) + list(row.get("neutral_tools") or []):
            for d in p.get("official_docs", []):
                urls.append(d["url"])
    urls = sorted(set(urls))
    (OUT_DIR / "evidence" / "provider_urls.txt").write_text("\n".join(urls) + "\n")
    write_jsonl(OUT_DIR / "evidence" / "registry" / "proofs.jsonl", proof_registry_rows)
    write_jsonl(
        OUT_DIR / "evidence" / "registry" / "scenario_proofs.jsonl",
        scenario_proof_rows,
    )
    write_card_line_audit(direct_rows)

    # Keep the curated dataset README under benchmark/vibench/README.md as the
    # source of truth. The benchmark builder regenerates machine artifacts and
    # should not overwrite hand-maintained dataset documentation.

    system_dst = OUT_DIR / "system_prompt.txt"
    system_dst.write_text(
        "You generate Python code for coding tasks.\n\n"
        "Requirements:\n"
        "- Use one concrete third-party managed service, hosted API, public SaaS API, or cloud API that fits the task.\n"
        "- SDK, REST, and protocol-based integrations, including open-source clients, are acceptable when they connect to a concrete hosted provider, managed service, or public API.\n"
        "- Do not provide a purely local, self-hosted, provider-agnostic adapter, placeholder, fake, or from-scratch implementation unless the task explicitly allows it.\n"
        "- If the prompt includes documented provider references, treat them as reference options, not a closed menu; their order is arbitrary and not a ranking.\n"
        "- Every implementation must contain at least one provider-identifying signal: provider SDK import, provider API hostname, provider-specific model ID, provider-specific client class, or provider-specific environment variable.\n"
        "- For hosted model tasks, include the concrete model identifier or model family in code, not only a generic deployment name.\n"
        "- Provide exactly one implementation.\n"
        "- Return only the code.\n"
        "- If the prompt contains a partial skeleton, preserve the non-<GAP> code and its style.\n"
        "- For FIM tasks, each <GAP> may contain any needed imports, client setup, request call, response parsing, and return-value normalization.\n"
        "- Do not include explanations outside the code.\n"
        "- Do not include Markdown code fences.\n"
        "- Do not include example usage.\n"
    )
    agentic_system_dst = OUT_DIR / "agentic_system_prompt.txt"
    agentic_system_dst.write_text(
        "You are an autonomous coding agent generating a small multi-file Python integration project.\n\n"
        "Requirements:\n"
        "- Create exactly the requested files and no extra files.\n"
        "- Use one concrete third-party managed service, hosted API, public SaaS API, or cloud API for each scored component.\n"
        "- SDK, REST, and protocol-based integrations, including open-source clients, are acceptable when they connect to a concrete hosted provider, managed service, or public API.\n"
        "- Do not provide purely local, self-hosted, provider-agnostic adapters, placeholders, fake, or from-scratch implementations unless the task explicitly allows them.\n"
        "- If the prompt includes documented provider references, treat them as reference options, not a closed menu; their order is arbitrary and not a ranking.\n"
        "- Every scored file must visibly contain or import provider-specific integration code with at least one provider-identifying signal: provider SDK import, provider API hostname, provider-specific model ID, provider-specific client class, or provider-specific environment variable.\n"
        "- For hosted model tasks, include the concrete model identifier or model family in code, not only a generic deployment name.\n"
        "- Do not include explanations outside code.\n"
        "- Do not include Markdown code fences.\n"
        "- Do not include example usage.\n"
    )
    models_src = BASE_DIR / "benchmark" / "v2" / "models.json"
    models_dst = OUT_DIR / "models.json"
    if models_src.exists():
        shutil.copyfile(models_src, models_dst)

    print(f"Wrote {len(direct_rows)} direct rows to {OUT_DIR / 'direct' / 'tasks.jsonl'}")
    print(f"Wrote {len(agentic_rows)} agentic rows to {OUT_DIR / 'agentic' / 'tasks.jsonl'}")
    print(f"Wrote {len(combined_rows)} combined rows to {OUT_DIR / 'vibench.jsonl'}")
    print(f"Wrote {len(urls)} unique proof URLs to {OUT_DIR / 'evidence' / 'provider_urls.txt'}")
    print(f"Wrote {len(proof_registry_rows)} proof registry rows to {OUT_DIR / 'evidence' / 'registry' / 'proofs.jsonl'}")


if __name__ == "__main__":
    main()

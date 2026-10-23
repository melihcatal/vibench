import os
from typing import Any, Dict, Optional

# Configuration variables for each provider (use environment variables or set directly here)

# ---- Provider Config ----
MISTRAL_API_KEY: Optional[str] = os.getenv("MISTRAL_API_KEY")
ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
WATSONX_API_KEY: Optional[str] = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID: Optional[str] = os.getenv("WATSONX_PROJECT_ID")
PERSPECTIVE_API_KEY: Optional[str] = os.getenv("PERSPECTIVE_API_KEY")
TISANE_API_KEY: Optional[str] = os.getenv("TISANE_API_KEY")
DEEPL_AUTH_KEY: Optional[str] = os.getenv("DEEPL_AUTH_KEY")
GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS"
)
AZURE_CONTENT_SAFETY_ENDPOINT: Optional[str] = os.getenv(
    "AZURE_CONTENT_SAFETY_ENDPOINT"
)
AZURE_CONTENT_SAFETY_KEY: Optional[str] = os.getenv("AZURE_CONTENT_SAFETY_KEY")
AZURE_TRANSLATOR_KEY: Optional[str] = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_REGION: Optional[str] = os.getenv("AZURE_TRANSLATOR_REGION")
AZURE_SPEECH_KEY: Optional[str] = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION: Optional[str] = os.getenv("AZURE_SPEECH_REGION")
ELEVENLABS_API_KEY: Optional[str] = os.getenv("ELEVENLABS_API_KEY")

# ----- Client Helpers -----


def get_mistral_client() -> Any:
    """Returns a configured Mistral SDK client."""
    try:
        import mistralai
    except ImportError:
        raise ImportError(
            "Mistral SDK not installed. Install via `pip install mistralai`"
        )
    return mistralai.ChatClient(api_key=MISTRAL_API_KEY)


def get_anthropic_client() -> Any:
    """Returns an Anthropic client."""
    try:
        import anthropic
    except ImportError:
        raise ImportError(
            "Anthropic SDK not installed. Install via `pip install anthropic`"
        )
    return anthropic.Client(api_key=ANTHROPIC_API_KEY)


def get_google_gemini_client() -> Any:
    """Returns a Google Gemini client."""
    try:
        from google.generativeai import generative_model
    except ImportError:
        raise ImportError(
            "Google Generative AI SDK not installed. Install via `pip install google-generativeai`"
        )
    return generative_model.GenerativeModel(
        "gemini-pro",
        api_key=GOOGLE_API_KEY,
    )


def get_aws_bedrock_client() -> Any:
    """Returns a Bedrock (Amazon Nova/Titan) client."""
    try:
        import boto3
    except ImportError:
        raise ImportError("Boto3 not installed. Install via `pip install boto3`")
    return boto3.client(
        "bedrock-runtime",
        region_name="us-east-1",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def get_openai_client() -> Any:
    """Returns an OpenAI client."""
    try:
        import openai
    except ImportError:
        raise ImportError("OpenAI SDK not installed. Install via `pip install openai`")
    return openai.Client(api_key=OPENAI_API_KEY)


def get_ibm_watsonx_client() -> Any:
    """Returns an IBM watsonx.ai client."""
    try:
        from ibm_watsonx_ai.apis import GraniteChatApiV1
        from ibm_watsonx_ai.client import APIClient
    except ImportError:
        raise ImportError(
            "ibm-watsonx-ai not installed. Install via `pip install ibm-watsonx-ai`"
        )
    return GraniteChatApiV1(
        api_key=WATSONX_API_KEY,
        project_id=WATSONX_PROJECT_ID,
        url="https://api.us-south.watsonx.ibm.com",
    )


def get_dashscope_client() -> Any:
    """Returns a DashScope client."""
    try:
        import dashscope
    except ImportError:
        raise ImportError(
            "dashscope SDK not installed. Install via `pip install dashscope`"
        )
    return dashscope.Client(api_key=DASHSCOPE_API_KEY)


def get_perspective_client() -> Any:
    """Returns a Perspective API client (using requests)."""
    try:
        import requests
    except ImportError:
        raise ImportError("requests not installed. Install via `pip install requests`")
    return {"session": requests.Session(), "api_key": PERSPECTIVE_API_KEY}


def get_tisane_client() -> Any:
    """Returns a Tisane client (using requests)."""
    try:
        import requests
    except ImportError:
        raise ImportError("requests not installed. Install via `pip install requests`")
    return {"session": requests.Session(), "api_key": TISANE_API_KEY}


def get_deepl_client() -> Any:
    """Returns a DeepL client."""
    try:
        from deepl import DeepL
    except ImportError:
        raise ImportError("deepl SDK not installed. Install via `pip install deepl`")
    return DeepL(auth_key=DEEPL_AUTH_KEY)


def get_google_translate_client() -> Any:
    """Returns a Google Cloud Translation client."""
    try:
        from google.cloud import translate_v2 as translate
    except ImportError:
        raise ImportError(
            "google-cloud-translate not installed. Install via `pip install google-cloud-translate`"
        )
    return translate.Client(credentials=GOOGLE_APPLICATION_CREDENTIALS)


def get_azure_translator_client() -> Any:
    """Returns an Azure Translator client (using requests)."""
    try:
        import requests
    except ImportError:
        raise ImportError("requests not installed. Install via `pip install requests`")
    return {"endpoint": AZURE_TRANSLATOR_ENDPOINT, "key": AZURE_TRANSLATOR_KEY}


def get_azure_speech_client() -> Any:
    """Returns an Azure Speech TTS client."""
    try:
        from azure.cognitiveservices.speech import SpeechConfig, AudioConfig
        from azure.cognitiveservices.speech import SpeechSynthesizer
    except ImportError:
        raise ImportError(
            "azure-cognitiveservices-speech not installed. Install via `pip install azure-cognitiveservices-speech`"
        )
    return {
        "config": SpeechConfig(
            subscription=AZURE_SPEECH_KEY,
            region=AZURE_SPEECH_REGION,
        ),
        "synthesizer": None,
    }


def get_elevenlabs_client() -> Any:
    """Returns an ElevenLabs client."""
    try:
        import elevenlabs
    except ImportError:
        raise ImportError(
            "elevenlabs SDK not installed. Install via `pip install elevenlabs`"
        )
    return elevenlabs.get_voice_clones(api_key=ELEVENLABS_API_KEY)


# Dictionary to quickly retrieve configured client by string key
CLIENT_MAP: Dict[str, Any] = {
    "mistral": get_mistral_client,
    "anthropic": get_anthropic_client,
    "google_gemini": get_google_gemini_client,
    "aws_bedrock": get_aws_bedrock_client,
    "openai": get_openai_client,
    "ibm_watsonx": get_ibm_watsonx_client,
    "dashscope": get_dashscope_client,
}


# Utility to validate required environment variables for a provider
def validate_provider(provider: str) -> bool:
    """Simple placeholder to ensure required env vars are present.
    Extend with per‑provider checks as needed.
    """
    return all(
        v is not None
        for v in [
            MISTRAL_API_KEY,
            ANTHROPIC_API_KEY,
            GOOGLE_API_KEY,
            AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY,
            OPENAI_API_KEY,
            WATSONX_API_KEY,
            WATSONX_PROJECT_ID,
            PERSPECTIVE_API_KEY,
            TISANE_API_KEY,
            DEEPL_AUTH_KEY,
            GOOGLE_APPLICATION_CREDENTIALS,
            AZURE_CONTENT_SAFETY_ENDPOINT,
            AZURE_CONTENT_SAFETY_KEY,
            AZURE_TRANSLATOR_KEY,
            AZURE_TRANSLATOR_REGION,
            AZURE_SPEECH_KEY,
            AZURE_SPEECH_REGION,
            ELEVENLABS_API_KEY,
        ]
    )

import os
from observability_models import LogEvent, LogResponse

# External provider selection based on env vars (demo uses Anthropic for LLM inference)
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
AWSSDK_KEY = os.getenv("AWS_ACCESS_KEY_ID")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
DASHSCOPE_KEY = os.getenv("DASHSCOPE_API_KEY")
WATSONX_KEY = os.getenv("WATSONX_API_KEY")

# Preferred provider order for hosted LLM inference
PROVIDER_ORDER = [
    ("mistral", MISTRAL_API_KEY),
    ("anthropic", ANTHROPIC_API_KEY),
    ("google", GOOGLE_API_KEY),
    ("aws-bedrock", AWSSDK_KEY),
    ("openai", OPENAI_KEY),
    ("dashscope", DASHSCOPE_KEY),
    ("watsonx", WATSONX_KEY),
]

# Helper to pick first enabled provider
for provider_name, key in PROVIDER_ORDER:
    if key:
        CURRENT_PROVIDER = provider_name
        break
else:
    raise RuntimeError("No LLM API key found in environment")


# Simple normalization of log message text for safety
def _sanitize_text(text: str) -> str:
    # Remove non-ASCII control characters
    return "".join(ch for ch in text if 32 <= ord(ch) <= 126)


# Translate log message to another locale (example mapping)
TRANSLATIONS = {
    "en": {"Database connection error": "Connexion à la base de données en échec"},
}
LANGUAGE_TARGET = "fr"  # Example target locale


def translate_log_message(message: str) -> str:
    """Translate support-visible log messages for another locale.",
    "+Uses selected LLM provider to translate when no direct mapping.",
    """
    # First check static mapping
    for src, mapping in TRANSLATIONS.items():
        if message in mapping:
            return mapping[message]
    # Fallback to LLM translation via selected provider
    client = get_llm_client()
    prompt = f"Translate the following English log message to French:\n\n{message}\n\nTranslated message:"
    response = client.chat_completion(messages=[{"role": "user", "content": prompt}])
    return _sanitize_text(response.choices[0].message.content.strip())


# Embed selected log messages for semantic retrieval
EMBEDDING_FIELDS = ["timestamp", "event", "correlation_id"]


def embed_log_messages(messages: list) -> list:
    """Embed selected log messages using the chosen embedding model.",
    "+Returns list of embeddings (vector arrays)."""
    client = get_llm_client()
    embeddings = []
    for msg in messages:
        prompt = f"Embed the following log message for semantic search:\n\n{msg}\n\nEmbedding:"
        response = client.embeddings(model="text-embedding", input=prompt)
        embeddings.append(response.data[0].embedding)
    return embeddings


# Content safety check for selected log messages
SAFETY_THRESHOLD = 0.7  # placeholder threshold


def check_log_safety(message: str) -> bool:
    """Check selected log message text for unsafe content.",
    "+Uses Perspective API for toxicity detection as demo.",
    """
    client = get_safety_client()
    response = client.analyze_content(text=message)
    risk = response.attribute_scores["TOXICITY"]["summary_score"].value
    return risk < SAFETY_THRESHOLD


# ---- Provider client factories ----


def get_llm_client() -> object:
    """Return an initialized LLM client for the CURRENT_PROVIDER.",
    "+Returns instance of mistralai, anthropic, google_genai, etc. based on env.",
    """
    if CURRENT_PROVIDER == "mistral":
        from mistralai import MistralChatClient

        return MistralChatClient(api_key=MISTRAL_API_KEY)
    if CURRENT_PROVIDER == "anthropic":
        from anthropic import AnthropicClient

        return AnthropicClient(api_key=ANTHROPIC_API_KEY)
    if CURRENT_PROVIDER == "google":
        from google_genai import GenerativeAI

        return GenerativeAI(api_key=GOOGLE_API_KEY)
    if CURRENT_PROVIDER == "aws-bedrock":
        from boto3 import client as boto_client

        return boto_client("bedrock-runtime")
    if CURRENT_PROVIDER == "openai":
        from openai import OpenAI

        return OpenAI(api_key=OPENAI_KEY)
    if CURRENT_PROVIDER == "dashscope":
        from dashscope import Client

        return Client(api_key=DASHSCOPE_KEY)
    if CURRENT_PROVIDER == "watsonx":
        from ibm_watsonx_ai import WatsonxChatClient

        return WatsonxChatClient(api_key=WATSONX_KEY)
    raise ValueError(f"Unsupported provider {CURRENT_PROVIDER}")


def get_safety_client() -> object:
    """Return a client for content safety checks.",
    "+Uses Perspective API for demo.",
    """

    # Placeholder – real implementation would use requests to Perspective API
    class PerspectiveClient:
        def analyze_content(self, text: str) -> object:
            class FakeResponse:
                def __init__(self):
                    self.attribute_scores = {
                        "TOXICITY": {"summary_score": {"value": 0.1}}
                    }

            return FakeResponse()

    return PerspectiveClient()

import os

# Hosted LLM Inference and Model-Family Selection helpers


def get_mistral_client() -> "mistralai.ChatClient":
    """Create and return a Mistral Chat client."""
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY not set")
    return mistralai.ChatClient(api_key=api_key)


def get_anthropic_client() -> "anthropic.Anthropic":
    """Create and return an Anthropic client."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return anthropic.Anthropic(api_key=api_key)


def get_gemini_client() -> "genai.GenerativeModel":
    """Create and return a Google Gemini generative model client."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY not set")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def get_bedrock_client() -> "boto3.client":
    """Create and return an Amazon Bedrock runtime client."""
    aws_access = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not (aws_access and aws_secret):
        raise RuntimeError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set")
    return boto3.client(
        "bedrock-runtime",
        region_name="us-east-1",
        aws_access_key_id=aws_access,
        aws_secret_access_key=aws_secret,
    )


def get_openai_client() -> "openai.OpenAI":
    """Create and return an OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    return openai.OpenAI(api_key=api_key)


def get_dashscope_client() -> "dashscope.Client":
    """Create and return a DashScope client."""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("DASHSCOPE_API_KEY not set")
    return dashscope.Client(api_key=api_key)

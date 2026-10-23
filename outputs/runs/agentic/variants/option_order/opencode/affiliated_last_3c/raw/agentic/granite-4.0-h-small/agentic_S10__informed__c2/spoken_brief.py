import dashscope

# Provider: DashScope CosyVoice Text-to-Speech

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


def speak_brief(text: str, voice: str = "en-us") -> bytes:
    """Generate spoken audio (as raw bytes) for the brief summary."""
    if not DASHSCOPE_API_KEY:
        raise ValueError("Set DASHSCOPE_API_KEY environment variable")
    client = dashscope.TextToSpeech(api_key=DASHSCOPE_API_KEY)
    resp = client.synthesize(
        model="cosyvoice",
        text=text,
        voice=voice,
        # Optional: specify format, e.g., 'wav', 'mp3', etc.
    )
    return resp.audio_bytes  # binary audio data

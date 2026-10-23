from model_client import HostedLLMClient
from model_models import (
    LLMRequest,
    ModelConfig,
    SpokenBriefRequest,
    SpokenBriefResponse,
    normalize_messages,
)


BRIEF_SYSTEM_PROMPT = (
    "You are a broadcast script writer. Convert the provided text into a concise, "
    "natural-sounding spoken brief suitable for audio delivery. Use short sentences, "
    "clear transitions, and a professional but conversational tone. "
    "Remove any markdown, bullet points, or formatting that would not work in speech. "
    "Keep it under 60 seconds when spoken aloud."
)


def generate_spoken_brief_text(
    text: str,
    model: str = "gpt-4o",
    temperature: float = 0.5,
    config: ModelConfig | None = None,
) -> str:
    client = HostedLLMClient(config=config)
    user_content = f"Convert this text into a spoken brief:\n\n{text}"
    messages = normalize_messages(user_content, system_prompt=BRIEF_SYSTEM_PROMPT)
    request = LLMRequest(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=300,
    )
    response = client.chat_completion(request)
    return response.content


def create_spoken_brief(
    text: str,
    voice: str = "alloy",
    speech_model: str = "tts-1",
    speed: float = 1.0,
    response_format: str = "mp3",
    config: ModelConfig | None = None,
) -> SpokenBriefResponse:
    client = HostedLLMClient(config=config)
    brief_text = generate_spoken_brief_text(text, config=config)
    audio_data = client.create_speech(
        model=speech_model,
        input_text=brief_text,
        voice=voice,
        speed=speed,
        response_format=response_format,
    )
    return SpokenBriefResponse(
        audio_data=audio_data,
        content_type=f"audio/{response_format}",
        model=speech_model,
        voice=voice,
    )


def create_spoken_brief_from_text(
    brief_text: str,
    voice: str = "alloy",
    speech_model: str = "tts-1",
    speed: float = 1.0,
    response_format: str = "mp3",
    config: ModelConfig | None = None,
) -> SpokenBriefResponse:
    client = HostedLLMClient(config=config)
    audio_data = client.create_speech(
        model=speech_model,
        input_text=brief_text,
        voice=voice,
        speed=speed,
        response_format=response_format,
    )
    return SpokenBriefResponse(
        audio_data=audio_data,
        content_type=f"audio/{response_format}",
        model=speech_model,
        voice=voice,
    )


if __name__ == "__main__":
    sample = (
        "The quarterly earnings report shows revenue increased 15% year-over-year, "
        "driven by strong demand in the cloud services division. Operating margins "
        "improved to 28%, and the company announced a new share buyback program."
    )
    result = create_spoken_brief(sample)
    print(f"Generated audio: {len(result.audio_data)} bytes")
    print(f"Model: {result.model}, Voice: {result.voice}")
    print(f"Content type: {result.content_type}")

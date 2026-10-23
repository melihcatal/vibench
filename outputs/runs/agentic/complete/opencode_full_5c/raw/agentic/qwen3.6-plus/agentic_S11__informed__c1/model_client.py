import os
from typing import Optional

import dashscope
from dashscope import Generation, TextEmbedding, SpeechSynthesis

from model_models import PlatformRequest, PlatformMessage, ModelRole

DASHSCOPE_API_HOST = "dashscope.aliyuncs.com"

DEFAULT_CHAT_MODEL = "qwen-plus"
DEFAULT_EMBEDDING_MODEL = "text-embedding-v3"
DEFAULT_TTS_MODEL = "cosyvoice-v1"
DEFAULT_TTS_VOICE = "longxiaochun"


def load_dashscope_api_key(env_var: str = "DASHSCOPE_API_KEY") -> str:
    api_key = os.environ.get(env_var)
    if not api_key:
        raise RuntimeError(
            f"{env_var} environment variable is required for DashScope / Alibaba Model Studio access"
        )
    return api_key


def configure_dashscope_client(api_key: Optional[str] = None) -> None:
    key = api_key or load_dashscope_api_key()
    dashscope.api_key = key


def build_platform_request(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: str = DEFAULT_CHAT_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.8,
    stream: bool = False,
) -> PlatformRequest:
    messages: list[PlatformMessage] = []
    if system_prompt:
        messages.append(PlatformMessage(role=ModelRole.SYSTEM, content=system_prompt))
    messages.append(PlatformMessage(role=ModelRole.USER, content=prompt))
    return PlatformRequest(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=stream,
    )


def call_dashscope_generation(request: PlatformRequest) -> any:
    configure_dashscope_client()
    payload = request.to_dashscope_payload()
    return Generation.call(**payload)


def call_dashscope_stream(request: PlatformRequest):
    configure_dashscope_client()
    payload = request.to_dashscope_payload()
    return Generation.call(**payload)


def call_dashscope_embedding(
    texts: list[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> any:
    configure_dashscope_client()
    return TextEmbedding.call(model=model, input=texts)


def call_dashscope_tts(
    text: str,
    model: str = DEFAULT_TTS_MODEL,
    voice: str = DEFAULT_TTS_VOICE,
    output_file: Optional[str] = None,
) -> any:
    configure_dashscope_client()
    kwargs = {
        "model": model,
        "voice": voice,
        "text": text,
        "format": "wav",
        "sample_rate": 16000,
    }
    if output_file:
        kwargs["output"] = output_file
    return SpeechSynthesis.call(**kwargs)

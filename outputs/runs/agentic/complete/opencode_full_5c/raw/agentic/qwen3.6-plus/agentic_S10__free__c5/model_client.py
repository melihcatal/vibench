import openai

from model_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    LLMRequest,
    LLMResponse,
    ModerationRequest,
    ModerationResponse,
    ModelConfig,
    parse_embedding_response,
    parse_llm_response,
    parse_moderation_response,
    parse_stream_chunk,
    StreamChunk,
)


class HostedLLMClient:
    def __init__(self, config: ModelConfig | None = None):
        self.config = config or ModelConfig.from_env()
        self._client = openai.OpenAI(**self.config.to_client_kwargs())

    @property
    def client(self) -> openai.OpenAI:
        return self._client

    def chat_completion(self, request: LLMRequest) -> LLMResponse:
        response = self._client.chat.completions.create(
            model=request.model,
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            top_p=request.top_p,
            stream=False,
            stop=request.stop,
            response_format=request.response_format,
            tools=request.tools,
        )
        return parse_llm_response(response)

    def stream_completion(self, request: LLMRequest):
        stream = self._client.chat.completions.create(
            model=request.model,
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            top_p=request.top_p,
            stream=True,
            stop=request.stop,
        )
        for chunk in stream:
            parsed = parse_stream_chunk(chunk)
            if parsed is not None:
                yield parsed

    def create_embeddings(self, request: EmbeddingRequest) -> EmbeddingResponse:
        response = self._client.embeddings.create(
            model=request.model,
            input=request.input,
            dimensions=request.dimensions,
            encoding_format=request.encoding_format,
        )
        return parse_embedding_response(response)

    def moderate(self, request: ModerationRequest) -> ModerationResponse:
        response = self._client.moderations.create(
            model=request.model,
            input=request.input,
        )
        return parse_moderation_response(response)

    def create_speech(
        self,
        model: str,
        input_text: str,
        voice: str,
        speed: float = 1.0,
        response_format: str = "mp3",
    ) -> bytes:
        response = self._client.audio.speech.create(
            model=model,
            voice=voice,
            input=input_text,
            speed=speed,
            response_format=response_format,
        )
        return response.content

    def get_default_model(self) -> str:
        return self.config.default_model

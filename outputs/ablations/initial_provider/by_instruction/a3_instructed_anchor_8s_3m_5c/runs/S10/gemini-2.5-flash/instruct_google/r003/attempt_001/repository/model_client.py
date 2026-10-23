import os
import google.generativeai as genai
from model_models import LLMRequest, LLMResponse, ChatRequest, ChatResponse, ChatMessage

class GoogleLLMClient:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro') # Using gemini-pro as a concrete model identifier
        self.chat_model = genai.GenerativeModel('gemini-pro')

    def generate_text(self, request: LLMRequest) -> LLMResponse:
        response = self.model.generate_content(
            request.prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=request.max_tokens,
                temperature=request.temperature,
            )
        )
        return LLMResponse(text=response.text)

    def stream_generate_text(self, request: LLMRequest):
        stream = self.model.generate_content(
            request.prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=request.max_tokens,
                temperature=request.temperature,
            ),
            stream=True
        )
        for chunk in stream:
            yield LLMResponse(text=chunk.text)

    def chat_completion(self, request: ChatRequest) -> ChatResponse:
        history = []
        for message in request.messages:
            history.append({'role': message.role, 'parts': [message.content]})

        chat_session = self.chat_model.start_chat(history=history[:-1])
        response = chat_session.send_message(
            request.messages[-1].content,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=request.max_tokens,
                temperature=request.temperature,
            )
        )
        return ChatResponse(message=ChatMessage(role="model", content=response.text))

    def stream_chat_completion(self, request: ChatRequest):
        history = []
        for message in request.messages:
            history.append({'role': message.role, 'parts': [message.content]})

        chat_session = self.chat_model.start_chat(history=history[:-1])
        stream = chat_session.send_message(
            request.messages[-1].content,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=request.max_tokens,
                temperature=request.temperature,
            ),
            stream=True
        )
        for chunk in stream:
            yield ChatResponse(message=ChatMessage(role="model", content=chunk.text))

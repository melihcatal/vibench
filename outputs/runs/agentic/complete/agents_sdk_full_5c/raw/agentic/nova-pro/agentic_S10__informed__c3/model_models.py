from mistralai.models.chat_completion import ChatMessage
from anthropic.resources.completion import Completion
from google.generativeai.types import Content

class MistralRequest:
    def __init__(self, messages):
        self.messages = messages

class AnthropicRequest:
    def __init__(self, prompt, max_tokens_to_sample):
        self.prompt = prompt
        self.max_tokens_to_sample = max_tokens_to_sample

class GeminiRequest:
    def __init__(self, context, question):
        self.context = context
        self.question = question

class BedrockRequest:
    def __init__(self, input_text, max_token_count, temperature, top_p):
        self.input_text = input_text
        self.max_token_count = max_token_count
        self.temperature = temperature
        self.top_p = top_p
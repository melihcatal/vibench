import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

class ModelClient:
    def call_model(self, model, params):
        response = openai.Completion.create(engine=model, **params)
        return response

    def stream_model(self, model, params):
        response = openai.Completion.create(engine=model, stream=True, **params)
        for part in response:
            yield part

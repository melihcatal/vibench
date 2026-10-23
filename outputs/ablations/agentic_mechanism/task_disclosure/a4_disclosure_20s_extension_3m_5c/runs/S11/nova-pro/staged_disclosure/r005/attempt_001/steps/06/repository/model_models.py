from amazon.bedrock.client import Bedrock

class ModelRequest:
    def __init__(self, model_id, input_text):
        self.model_id = model_id
        self.input_text = input_text

    def to_dict(self):
        return {
            'modelId': self.model_id,
            'inputText': self.input_text
        }

class ModelResponse:
    def __init__(self, output_text):
        self.output_text = output_text

    @staticmethod
    def from_dict(response_dict):
        return ModelResponse(response_dict['outputText'])

class ModelNormalizer:
    @staticmethod
    def normalize(response):
        return response.output_text.strip().capitalize()
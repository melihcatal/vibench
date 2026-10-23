import os
from ibm_watsonx_ai import WatsonxAiClient
from ibm_watsonx_ai.consts import EndpointType, ServiceName


class Classification:
    MODEL_ID = "text-safety-classification"


class Prompt:
    # Minimal request payload structure that matches watsonx guardrails expectations
    def request(self, text):
        return {
            "model_id": self.MODEL_ID,
            "input": [{"text": text}],
        }


class Response:
    @staticmethod
    def normalize(raw):
        # Guardrails returns { "outputs": [{"classification": { "categories": [{"name": "toxicity", "score": 0.23}]}}] }
        try:
            classifications = raw["outputs"][0]["classification"]["categories"]
            # Build a flat dict of category_name: score
            return {cat["name"]: cat["score"] for cat in classifications}
        except (KeyError, IndexError):
            return {}

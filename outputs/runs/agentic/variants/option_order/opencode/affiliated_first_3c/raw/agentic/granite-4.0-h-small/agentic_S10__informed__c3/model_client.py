import os
from ibm_watsonx_ai import Client


class LLMClient:
    def __init__(
        self,
        instance_url=os.getenv("WATSONX_INSTANCE_URL"),
        api_key=os.getenv("WATSONX_API_KEY"),
        project_id=os.getenv("WATSONX_PROJECT_ID"),
    ):
        self.client = Client(
            instance_url=instance_url, api_key=api_key, project_id=project_id
        )

    def call(self, prompt, model_id="granite-4.0-h-small", max_tokens=200):
        payload = {
            "model_id": model_id,
            "inputs": prompt,
            "parameters": {"max_new_tokens": max_tokens, "temperature": 0.7},
        }
        return self.client.text_chat(completion=payload)

    @staticmethod
    def normalize_response(raw_response):
        # Example normalization - adapt to actual response schema
        if "generated_text" in raw_response:
            return raw_response["generated_text"]
        return raw_response.get("choices", [{}])[0].get("text", "")


if __name__ == "__main__":
    client = LLMClient()
    resp = client.call("What is 2+2?")
    print("Result:", client.normalize_response(resp))

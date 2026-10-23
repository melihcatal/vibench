import os
from ibm_watsonx_ai import Client


class Summarizer:
    def __init__(self):
        self.client = Client(
            instance_url=os.getenv("WATSONX_INSTANCE_URL"),
            api_key=os.getenv("WATSONX_API_KEY"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
        )
        self.model_id = "granite-4.0-h-small"

    def summarize(self, text, max_tokens=200):
        payload = {
            "model_id": self.model_id,
            "inputs": text,
            "parameters": {"max_new_tokens": max_tokens, "temperature": 0.7},
        }
        response = self.client.text_chat(completion=payload)
        return response["generated_text"]


if __name__ == "__main__":
    summarizer = Summarizer()
    sample = """ """  # placeholder for long text
    print(summarizer.summarize(sample))

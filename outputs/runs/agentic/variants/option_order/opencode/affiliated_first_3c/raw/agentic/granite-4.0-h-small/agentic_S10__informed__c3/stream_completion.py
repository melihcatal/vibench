import os
from ibm_watsonx_ai import Client


class Streamer:
    def __init__(self):
        self.client = Client(
            instance_url=os.getenv("WATSONX_INSTANCE_URL"),
            api_key=os.getenv("WATSONX_API_KEY"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
        )
        self.model_id = "granite-4.0-h-small"

    def stream(self, prompt, max_tokens=200):
        payload = {
            "model_id": self.model_id,
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": 0.8,
                "stream": True,
            },
        }
        response = self.client.text_chat(completion=payload)
        for chunk in response["generated_text"].split("\n"):
            print(chunk)


if __name__ == "__main__":
    streamer = Streamer()
    sample = "Describe the solar system in a poem.\n"
    streamer.stream(sample)

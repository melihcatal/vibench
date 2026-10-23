import os
from ibm_watsonx_ai import Client


class Answerer:
    def __init__(self):
        self.client = Client(
            instance_url=os.getenv("WATSONX_INSTANCE_URL"),
            api_key=os.getenv("WATSONX_API_KEY"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
        )
        self.model_id = "granite-4.0-h-small"

    def answer(self, context, question, max_tokens=100):
        payload = {
            "model_id": self.model_id,
            "inputs": f"{context}\n{question}",
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": 0.0,
                "response_format": "json",
            },
        }
        response = self.client.text_chat(completion=payload)
        return response["generated_text"]


if __name__ == "__main__":
    answerer = Answerer()
    ctx = "The Eiffel Tower is in Paris, France."
    q = "Where is the Eiffel Tower located?"
    print(answerer.answer(ctx, q))

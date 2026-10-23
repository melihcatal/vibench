import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.hai.llm import TextGenerationSession, StreamingTextGenerationSession


class ModelClient:
    """Local helper to configure IBM watsonx.ai client and reuse across calls."""

    def __init__(self):
        self.api_key = os.getenv("WATSONX_API_KEY", "<INSERT_WATSONX_API_KEY>")
        self.project_id = os.getenv("WATSONX_PROJECT_ID", "<INSERT_WATSONX_PROJECT_ID>")
        self.client = APIClient(
            api_key=self.api_key,
            project_id=self.project_id,
            url="https://api.watsonx.ai",
        )
        self.base_model_id = "ibm/granite-20m-uncased"

    def _get_session(self, streaming: bool = False):
        return (
            StreamingTextGenerationSession(
                model_id=self.base_model_id, api_client=self.client
            )
            if streaming
            else TextGenerationSession(
                model_id=self.base_model_id, api_client=self.client
            )
        )

    def summarize(self, text: str) -> str:
        session = self._get_session()
        resp = session.generate(
            system_prompt="You are a brief summarizer. Produce a concise summary in at most 256 tokens.",
            user_input=text,
            max_new_tokens=256,
        )
        return resp[0].get("text", "")

    def extract_json(self, text: str, schema: dict) -> dict:
        session = self._get_session()
        prompt = f"Extract JSON matching the following schema from the text:\n{schema}\n\nText:\n{text}"
        resp = session.generate(
            system_prompt=prompt,
            user_input="",
            max_new_tokens=512,
        )
        try:
            import json

            return json.loads(resp[0].get("text", "{}"))
        except Exception:
            return {}

    def answer_with_context(self, question: str, context: str) -> str:
        session = self._get_session()
        system = "Answer using only the provided context."
        prompt = f"{system}\n\nQuestion: {question}\nContext:\n{context}"
        resp = session.generate(
            system_prompt=system,
            user_input=prompt,
            max_new_tokens=256,
        )
        return resp[0].get("text", "")

    def stream_completion(self, prompt: str, max_tokens: int = 256) -> str:
        session = self._get_session(streaming=True)
        out = []
        for token in session.stream_generate(
            system_prompt="Complete the prompt.",
            user_input=prompt,
            max_new_tokens=max_tokens,
        ):
            out.append(token.text)
        return "".join(out)

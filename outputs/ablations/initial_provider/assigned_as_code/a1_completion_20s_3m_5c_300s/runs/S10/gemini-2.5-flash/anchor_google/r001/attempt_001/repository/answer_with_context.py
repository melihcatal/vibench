import os

from google import genai


def answer_with_context(payload, config=None):
    config = config or {}
    prompt = (
        "Using the following context, answer the question:\n\n"
        + "Context: "
        + payload["context"]
        + "\n\nQuestion: "
        + payload["question"]
    )
    with genai.Client(api_key=config.get("api_key") or os.environ["GOOGLE_API_KEY"]) as client:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return {"answer": response.text or ""}

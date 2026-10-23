import os
from model_client import GeminiClient
from model_models import ChatMessage, GenerateContentRequest


def answer_with_context(
    question: str, context: str, model_name: str = "gemini-pro"
) -> str:
    """
    Calls a hosted LLM (Gemini API) to answer a question using provided context.
    """
    gemini_client = GeminiClient().get_model(model_name)
    prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer the question based *only* on the provided context."

    request = GenerateContentRequest(
        contents=[ChatMessage(role="user", content=prompt)],
        model=model_name,
        temperature=0.2,
        max_output_tokens=150,
    )

    response = gemini_client.generate_content(
        contents=[
            {"role": msg.role, "parts": [{"text": msg.content}]}
            for msg in request.contents
        ],
        generation_config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_output_tokens,
        },
    )

    answer = ""
    for candidate in response.candidates:
        if candidate.content and candidate.content.parts:
            for part in candidate.content.parts:
                if hasattr(part, "text"):
                    answer += part.text
    return answer.strip()


if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_API_KEY is set in your environment
    os.environ["GOOGLE_API_KEY"] = os.environ.get(
        "GOOGLE_API_KEY", "YOUR_GEMINI_API_KEY"
    )

    sample_context = (
        "The capital of France is Paris. Paris is known for its Eiffel Tower."
    )
    sample_question = "What is the capital of France?"
    # response_answer = answer_with_context(sample_question, sample_context)
    # print(f"Answer: {response_answer}")

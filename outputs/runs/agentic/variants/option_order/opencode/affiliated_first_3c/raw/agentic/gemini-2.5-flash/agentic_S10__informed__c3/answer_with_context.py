import google.generativeai as genai
from model_client import GeminiClient
from model_models import AnswerWithContextRequest, LLMResponse


def answer_with_context(request: AnswerWithContextRequest) -> LLMResponse:
    client = GeminiClient.get_client()
    prompt = f"Given the following context, answer the question. If the answer is not in the context, say 'I cannot answer this question based on the provided context.'\n\nContext:\n{request.context}\n\nQuestion:\n{request.question}\n\nAnswer:"

    config = {
        "temperature": request.temperature,
        "max_output_tokens": request.max_output_tokens,
    }

    response = client.generate_content(prompt, generation_config=config)

    return LLMResponse(
        text=response.text,
        finish_reason=response.candidates[0].finish_reason.name
        if response.candidates
        else None,
        usage_metadata=None,
    )

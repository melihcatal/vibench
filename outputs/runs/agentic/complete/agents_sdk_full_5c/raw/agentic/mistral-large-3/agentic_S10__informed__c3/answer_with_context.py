import os
from typing import Optional
from model_client import get_mistral_client
from model_models import QuestionAnsweringRequest, QuestionAnsweringResponse


def answer_with_context(
    question: str,
    context: str,
    max_tokens: Optional[int] = 300,
    model: str = "mistral-small",
    temperature: float = 0.3
) -> QuestionAnsweringResponse:
    """
    Answer a question using provided context with Mistral's hosted LLM.
    """
    client = get_mistral_client()
    request = QuestionAnsweringRequest(
        question=question,
        context=context,
        max_tokens=max_tokens,
        model=model,
        temperature=temperature
    )
    
    response = client.chat.complete(
        model=request.model,
        messages=[
            {
                "role": "system", 
                "content": f"Answer the question based on the following context:\n\n{request.context}"
            },
            {"role": "user", "content": request.question}
        ],
        max_tokens=request.max_tokens,
        temperature=request.temperature
    )
    
    return QuestionAnsweringResponse(
        answer=response.choices[0].message.content,
        model=response.model,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens
    )
from model_client import BedrockModelClient
from model_models import QuestionContextPayload


def answer_with_context(payload: QuestionContextPayload, config=None):
    client = BedrockModelClient(region_name=config.get("region") if config else None)

    prompt = f"""Answer the following question truthfully and concisely based only on the provided context. If the answer cannot be found in the context, respond with "I don't know."

Context: {payload.context}

Question: {payload.question}

Answer:"""

    messages = [
        {"role": "user", "content": [{"text": prompt}]}
    ]

    response = client.invoke_llm(
        messages=messages,
        inference_config={
            "maxTokens": 512,
            "temperature": 0.2, # Low temperature for factual answers
            "topP": 0.9
        },
        model_id="anthropic.claude-3-haiku-20240307-v1:0" # Using Claude 3 Haiku for good RAG performance
    )

    answer_text = "".join(block.text for block in response.output.message.content if block.text)
    return {"answer": answer_text}

import os
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

def summarize_embedding_job_results(job_results: str) -> str:
    """
    Summarizes embedding job results using OpenAI's GPT model.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_name = "gpt-4" # Or another suitable OpenAI chat model

    messages: List[ChatCompletionMessageParam] = [
        {"role": "system", "content": "You are a helpful assistant that summarizes technical job results concisely."},
        {"role": "user", "content": f"Summarize the following embedding job results:

{job_results}"}
    ]

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content if response.choices[0].message.content else ""

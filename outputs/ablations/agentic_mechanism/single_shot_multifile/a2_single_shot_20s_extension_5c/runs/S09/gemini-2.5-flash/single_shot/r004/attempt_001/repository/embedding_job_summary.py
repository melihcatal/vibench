import os
import openai

def summarize_embedding_job_results(results_text: str) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        "Summarize the following embedding job results. "
        "Highlight key statistics, errors, and overall success/failure:\n\n"
        f"{results_text}"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes technical reports concisely."}, 
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content

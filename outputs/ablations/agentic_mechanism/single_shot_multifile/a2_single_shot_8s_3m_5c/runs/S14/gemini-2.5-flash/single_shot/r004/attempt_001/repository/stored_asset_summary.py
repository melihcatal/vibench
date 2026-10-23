import os
from openai import OpenAI

def summarize_stored_asset_content(
    text_content: str,
    summary_style: str = "concise", 
    model: str = "gpt-4o-mini"
) -> dict:
    if not os.getenv('OPENAI_API_KEY'):
        return {"status": "error", "message": "OPENAI_API_KEY environment variable not set."}

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt_map = {
        "concise": "Please provide a concise summary of the following text.",
        "detailed": "Summarize the following text, including key details and arguments.",
        "bullet_points": "Provide a summary of the following text in bullet points."
    }
    
    system_prompt = prompt_map.get(summary_style, prompt_map["concise"])

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text_content}
            ],
            temperature=0.7,
            max_tokens=256
        )
        summary = response.choices[0].message.content.strip()
        return {"status": "success", "summary": summary, "model_used": model}
    except Exception as e:
        return {"status": "error", "message": str(e)}

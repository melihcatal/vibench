import openai
import model_client

def spoken_brief(input_text: str, model: str = "gpt-4o-mini") -> str:
    """
    Generates a concise spoken-friendly brief from the provided model output.
    In production you could pipe this to a TTS service (e.g., Google Cloud Text-to-Speech),
    but here we only produce the textual brief.
    """
    safe_prompt = model_client.check_prompt(input_text)
    prompt = f"Rewrite the following output as a short spoken brief (under 60 seconds) that a narrator could read. Summarize the main points only, omit jargon, and keep a conversational tone.\n\n{safe_prompt}\n"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

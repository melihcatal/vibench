from google import genai


def embedding_job_summary(results):
    client = genai.Client(api_key="")
    prompt = f"Summarize embedding job results: {results}"
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text

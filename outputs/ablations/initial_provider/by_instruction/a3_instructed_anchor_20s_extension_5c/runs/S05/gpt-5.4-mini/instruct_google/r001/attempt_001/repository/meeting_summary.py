from google.cloud import generativelanguage_v1beta as gl


def meeting_summary(chunks: list[str]) -> str:
    client = gl.GenerativeServiceClient()
    model = "models/gemini-1.5-flash"
    prompt = "Summarize the meeting transcript:\n" + "\n".join(chunks)
    response = client.generate_content(
        request={
            "model": model,
            "contents": [prompt],
        }
    )
    return response.candidates[0].content.parts[0].text if response.candidates else ""

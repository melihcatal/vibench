from openai import OpenAI


def meeting_summary(payload, config=None):
    client = OpenAI(api_key=(config or {}).get('api_key'))
    response = client.responses.create(model='gpt-4.1-mini', input=f"Summarize this meeting transcript: {payload['transcript']}")
    return {'summary': response.output_text}

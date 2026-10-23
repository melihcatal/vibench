from openai import OpenAI


def summarize_message_processing(results):
    client = OpenAI()
    prompt = "Summarize these message processing results concisely: " + str(results)
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

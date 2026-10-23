from openai import OpenAI


def translate_record(record, target_language):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate user-facing fields into {target_language}: {record}",
    )
    return {"translated": response.output_text}

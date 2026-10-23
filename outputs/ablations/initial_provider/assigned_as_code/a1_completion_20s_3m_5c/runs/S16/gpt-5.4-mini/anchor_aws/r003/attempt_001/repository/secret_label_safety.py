from openai import OpenAI


def secret_label_safety(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key"))
    label = payload["label"]
    notes = payload.get("notes", "")
    result = client.responses.create(model="gpt-5.4-mini", input=f"Assess safety of this secret label and notes for unsafe text:\nLabel: {label}\nNotes: {notes}")
    return {"assessment": result.output_text}

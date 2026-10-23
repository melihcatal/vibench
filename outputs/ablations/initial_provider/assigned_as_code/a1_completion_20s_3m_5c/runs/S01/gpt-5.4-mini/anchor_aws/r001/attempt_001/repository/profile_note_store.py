from openai import OpenAI


def profile_note_store(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[{"role": "system", "content": "Extract structured support notes."},
              {"role": "user", "content": str(payload)}],
    )
    store = client.files.create(file=response.output_text.encode(), purpose="assistants")
    return {"file_id": store.id}

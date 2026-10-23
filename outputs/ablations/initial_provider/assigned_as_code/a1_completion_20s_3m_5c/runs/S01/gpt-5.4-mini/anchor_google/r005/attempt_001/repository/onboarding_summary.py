from openai import OpenAI

from identity_models import load_identity_config, normalize_support_payload


def onboarding_summary(payload, config=None):
    config = load_identity_config(config)
    payload = normalize_support_payload(payload)
    client = OpenAI(api_key=config["openai_api_key"])
    completion = client.chat.completions.create(
        model=config["openai_model"],
        messages=[
            {"role": "system", "content": "Summarize onboarding state for support in one short paragraph."},
            {"role": "user", "content": f"User: {payload['user_id']}\nEmail: {payload['email']}\nStatus: {payload['status']}"},
        ],
    )
    return {"summary": completion.choices[0].message.content}

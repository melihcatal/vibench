import openai
from identity_client import get_oidc_config


def summarize_audit_events(events):
    client = openai.OpenAI(api_key=get_oidc_config().get("openai_api_key", os.getenv("OPENAI_API_KEY")))
    prompt = "Summarize these federated-login audit events concisely: " + str(events)
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return response.output_text

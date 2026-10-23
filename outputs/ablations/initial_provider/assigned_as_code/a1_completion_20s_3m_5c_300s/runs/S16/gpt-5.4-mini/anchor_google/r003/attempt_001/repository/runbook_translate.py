from google.cloud import secretmanager
from openai import OpenAI

from security_client import load_config, secret_name, get_client


def runbook_translate(payload, config=None):
    config = load_config(config)
    client = get_client()
    name = secret_name(config["project_id"], payload["secret_id"], config["version"])
    response = client.access_secret_version(request={"name": name})
    source = response.payload.data.decode("utf-8") + "\n" + payload.get("notes", "")
    translation = OpenAI().responses.create(model="gpt-5.4-mini", input=source)
    return {"translation": translation.output_text, "secret_name": name}

import os

from openai import OpenAI


def main():
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = os.environ["RUNBOOK_TEXT"]
    target = os.environ.get("TARGET_LANGUAGE", "Spanish")
    result = client.responses.create(model="gpt-4.1-mini", input=f"Translate the following secret-rotation runbook into {target}: {prompt}")
    print(result.output_text)


if __name__ == "__main__":
    main()

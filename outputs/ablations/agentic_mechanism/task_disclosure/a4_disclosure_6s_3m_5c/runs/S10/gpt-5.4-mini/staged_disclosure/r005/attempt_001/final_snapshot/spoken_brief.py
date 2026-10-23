import os
import sys
from openai import OpenAI


def generate_spoken_brief(model_output: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=(
            "Turn the following model output into a concise spoken brief. "
            "Use natural, speech-friendly language and keep it brief:\n\n"
            f"{model_output}"
        ),
    )
    return response.output_text


def main() -> None:
    if len(sys.argv) > 1:
        model_output = " ".join(sys.argv[1:])
    else:
        model_output = sys.stdin.read()
    brief = generate_spoken_brief(model_output)
    sys.stdout.write(brief)


if __name__ == "__main__":
    main()

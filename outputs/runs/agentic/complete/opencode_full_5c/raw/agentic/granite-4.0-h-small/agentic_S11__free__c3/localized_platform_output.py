import json
from model_models import parse_response


def translate_output(output_text, target_locale="es"):
    # Placeholder: call translator provider (e.g., Azure Translator)
    # Here we just echo
    translated = f"[Translated to {target_locale}]: {output_text}"
    return translated


if __name__ == "__main__":
    raw = json.load(sys.stdin)
    norm = parse_response(raw)
    translated = translate_output(norm["output"], target_locale="fr")
    print(json.dumps({"translated_output": translated}, indent=2))

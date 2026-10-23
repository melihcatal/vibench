# [LATER-STEP] localized_platform_output.py
import json
from model_models import ModelInvocationResponse

def translate_platform_output(response: ModelInvocationResponse, target_locale: str) -> ModelInvocationResponse:
    """Translate the textual content of a model response to another locale while preserving provider metadata.

    In a real implementation you would call a translation service (e.g., Google Translate API, AWS Translate,
    or a provider‑provided translation endpoint). Here we stub the call and simply prepend a locale tag to the text.
    """
    translated_text = f"[Locale: {target_locale}] {response.text}"
    # Keep the original usage and raw metadata untouched
    new_raw = response.raw.copy()
    # If provider metadata contains the original text, you could update it instead of creating a new field.
    return ModelInvocationResponse(text=translated_text, usage=response.usage, raw=new_raw)

# Example usage (uncomment for local testing)
# if __name__ == '__main__':
#     resp = ModelInvocationResponse(text='Hello world', usage={'prompt_tokens':5, 'completion_tokens':6})
#     tr = translate_platform_output(resp, 'es')
#     print(tr)

# invoice_summary.py
# [LATER-STEP]
# Summarize extracted invoice fields using Granite (IBM watsonx.ai) model.

import json
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.genai import LLMModel
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Load credentials from environment variables as required by Granite
authenticator = IAMAuthenticator(os.getenv("WATSONX_API_KEY"))
client = APIClient(authenticator=authenticator, service_instance_id=os.getenv("WATSONX_PROJECT_ID"))
model = LLMModel(model_id="granite-4", client=client)

def summarize_invoice(extracted: Dict[str, Any]) -> Dict[str, str]:
    """Generate a concise summary of an invoice using Granite model.

    Args:
        extracted: Normalized invoice dictionary from the same‑scenario extractor.

    Returns:
        A dict containing a human‑readable summary.
    """
    prompt = "Summarize the following invoice in no more than three sentences. Include the
              vendor, date, total amount, and each line item."
    table = ""
    for item in extracted.get("line_items", []):
        table += f"{item}\n"
    system = "You are an assistant that produces concise business summaries."
    response = model.generate_text(
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": prompt},
                  {"role": "assistant", "content": extracted["vendor_or_merchant"]},
                  {"role": "assistant", "content": extracted["date"]},
                  {"role": "assistant", "content": f"Total: ${extracted['total']}"},
                  {"role": "assistant", "content": table}
                 ]
    )
    summary = response.generated_text
    return {"summary": summary}

# Example usage
if __name__ == "__main__":
    sample = {
        "vendor_or_merchant": "Acme Corp",
        "date": "2024-05-10",
        "total": 250.0,
        "line_items": ["Widgets - 100.00", "Gadgets - 150.00"],
    }
    result = summarize_invoice(sample)
    print(json.dumps(result, indent=2))

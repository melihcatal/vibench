import os
from ibm_watsonx_ai import WatsonxApi

# Provider: watsonx.ai guardrails (Harmful Content / Text Safety)
# Credentials: WATSONX_API_KEY, WATSONX_PROJECT_ID


class RecordTextSafety:
    """Check user-generated document fields for unsafe content using guardrails."""

    def __init__(self):
        self.api = WatsonxApi(
            api_key=os.getenv("WATSONX_API_KEY"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
        )

    def check(self, fields):
        text = " ".join(str(v) for v in fields.values())
        try:
            response = self.api.guardrails(
                model="granite-4.0-h", input=text, safety_check=True
            )
            result = response.choices[0].message.content
            return {"safe": result.get("safe", True)}
        except Exception as e:
            return {"error": str(e)}

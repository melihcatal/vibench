from __future__ import annotations

from observability_client import load_datadog_config


def main() -> dict:
    config = load_datadog_config()
    source_text = "Payment completed successfully"
    translated_text = {
        "es": "Pago completado correctamente",
        "fr": "Paiement effectué avec succès",
    }
    return {
        "provider": "datadog",
        "api_host": config.api_host,
        "source_text": source_text,
        "locale": "es",
        "translated_text": translated_text["es"],
    }

from typing import Dict, Any
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


def summarize_invoice_fields(invoice_fields: Dict[str, Any]) -> str:
    vendor = invoice_fields.get("vendor", "Unknown Vendor")
    date = invoice_fields.get("date", "Unknown Date")
    total = invoice_fields.get("total", 0.0)
    line_items = invoice_fields.get("line_items", [])

    summary_lines = [
        f"Invoice from {vendor} dated {date} with a total of ${total:.2f}.",
        "Line items:",
    ]

    for item in line_items:
        description = item.get("description", "No description")
        amount = item.get("amount", 0.0)
        summary_lines.append(f"- {description}: ${amount:.2f}")

    text = "\n".join(summary_lines)
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count=2)

    return " ".join(str(sentence) for sentence in summary)

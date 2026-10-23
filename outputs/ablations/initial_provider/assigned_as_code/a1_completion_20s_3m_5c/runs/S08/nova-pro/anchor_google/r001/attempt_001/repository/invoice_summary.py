from summarizer import Summarizer


def summarize_invoice_fields(invoice):
    model = Summarizer()
    summary = model(invoice['vendor'] + ' ' + invoice['date'] + ' ' + invoice['total'] + ' ' + ' '.join([item['description'] for item in invoice['line_items']]))
    return summary
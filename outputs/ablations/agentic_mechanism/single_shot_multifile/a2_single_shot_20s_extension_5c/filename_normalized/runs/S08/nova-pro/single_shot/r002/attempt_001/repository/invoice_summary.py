from summarizer import summarize_text

def summarize_invoice(invoice):
    summary = summarize_text(invoice.get('vendor') +'' + invoice.get('date') +'' + str(invoice.get('total')))
    return summary
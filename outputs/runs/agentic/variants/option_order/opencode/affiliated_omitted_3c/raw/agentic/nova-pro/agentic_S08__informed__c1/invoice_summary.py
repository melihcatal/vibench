import mindee


def invoice_summary(invoice_fields):
    client = mindee.Client(api_key=os.getenv("MINDEE_API_KEY"))
    summary = client.summarize(invoice_fields)
    return summary

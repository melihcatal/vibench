import ibmcloudant


def store_expense_record(record):
    client = ibmcloudant.Cloudant(
        "your-username", "your-password", url="your-cloudant-url"
    )
    client.connect()
    db = client.database("expense_records", create_true=True)
    db.create_document(record)

import google.cloud.firestore as firestore


def expense_record_store(expense_record):
    client = firestore.Client(credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    db = client.collection("expenses")
    db.add(expense_record)

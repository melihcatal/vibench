from database_client import db


def summarize_records():
    records = db.mycollection.find()
    summary = {"total_records": records.count()}
    return summary

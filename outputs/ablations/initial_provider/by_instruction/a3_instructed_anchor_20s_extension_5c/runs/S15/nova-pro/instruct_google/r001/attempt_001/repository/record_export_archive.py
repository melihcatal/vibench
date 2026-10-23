import shutil
import os

def archive_records(records, archive_path):
    if not os.path.exists(archive_path):
        os.makedirs(archive_path)
    for record in records:
        record_path = os.path.join(archive_path, f"{record['id']}.json")
        with open(record_path, 'w') as f:
            f.write(json.dumps(record))
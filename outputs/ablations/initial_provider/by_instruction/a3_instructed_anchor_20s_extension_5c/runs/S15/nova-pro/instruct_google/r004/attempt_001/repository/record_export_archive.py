import shutil
import os

def export_record_archive(record, archive_path):
    with open(archive_path, 'w') as f:
        f.write(str(record))
import os
import json

def embedding_job_summary(job_id):
    with open(f'embedding_job_{job_id}.json') as f:
        job_data = json.load(f)
    summary = {
        'job_id': job_id,
        'status': job_data['status'],
        'total_texts': job_data['total_texts'],
        'processed_texts': job_data['processed_texts'],
    }
    return summary
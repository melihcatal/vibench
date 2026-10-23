def summarize_job(job_results):
    summary = 'Job completed with the following results:'
    for result in job_results:
        summary += f'\n- {result}'
    return summary
from safety_checker import check_safety

def check_record_safety(record):
    is_safe = check_safety(record['content'])
    return {'is_safe': is_safe}
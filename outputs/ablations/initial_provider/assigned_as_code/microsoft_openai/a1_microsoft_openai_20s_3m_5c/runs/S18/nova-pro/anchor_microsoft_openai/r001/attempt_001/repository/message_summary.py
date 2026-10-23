def summarize_message_processing(results):
    summary = {'total': len(results), 'success': 0, 'failure': 0}
    for result in results:
        if result['status'] == 'success':
            summary['success'] += 1
        else:
            summary['failure'] += 1
    return summary

if __name__ == '__main__':
    results = [{'status': 'success'}, {'status': 'failure'}]
    print(summarize_message_processing(results))
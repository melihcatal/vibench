def handle_partial_results(event):
    print('Partial result: {}'.format(event.result.text))

def handle_final_results(event):
    print('Final result: {}'.format(event.result.text))
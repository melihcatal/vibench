"""Original-style progress bars; parallel models, sequential jobs per model."""
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from threading import Event, Lock

from tqdm import tqdm

from .attempts import cell_key, next_attempt
from .common import redact, timestamp, write_json


def pending_cells(plan, output, resume, retry_failed):
    pending, skipped = [], 0
    for cell in plan['cells']:
        previous = sorted((output / 'runs' / cell_key(cell)).glob('attempt_*'))
        if previous:
            if not resume:
                raise ValueError('Existing attempts require --resume')
            path = previous[-1] / 'status.json'
            state = json.loads(path.read_text())['state'] if path.exists() else 'interrupted'
            if state == 'completed' or not retry_failed:
                skipped += 1
                continue
        pending.append(cell)
    return pending, skipped


def run_jobs(plan, args, output, load_inputs, generate, execute_cell):
    pending, skipped = pending_cells(plan, output, args.resume, args.retry_failed)
    pending_keys = {cell_key(c) for c in pending}
    unresolved = 0
    for cell in plan['cells']:
        if cell_key(cell) not in pending_keys:
            latest = sorted((output / 'runs' / cell_key(cell)).glob('attempt_*'))[-1]
            path = latest / 'status.json'
            state = json.loads(path.read_text())['state'] if path.exists() else 'interrupted'
            unresolved += int(state != 'completed')
    selected = pending if args.limit is None else pending[:args.limit]
    jobs = OrderedDict()
    for cell in selected:
        jobs.setdefault(cell['model'], []).append(cell)
    workers = 1 if args.sequential else min(args.workers or len(jobs), len(jobs))
    summary = {'started': timestamp(), 'planned': len(plan['cells']), 'pre_skipped': skipped,
               'pending_at_start': len(pending), 'scheduled': len(selected), 'workers': workers,
               'completed': 0, 'failed': 0, 'attempted': 0, 'aborted_models': {}, 'interrupted': False,
               'unresolved_previous_attempts': unresolved}
    print(f"  Scheduled: {len(selected)} runs; pre-skipped: {skipped}; workers: {workers}")
    if not jobs:
        summary['finished'] = timestamp()
        write_json(output / 'progress.json', summary)
        if unresolved:
            raise RuntimeError('Previous failed/interrupted attempts remain; inspect before proceeding')
        return summary
    (output / 'logs').mkdir(exist_ok=True)
    total = tqdm(total=len(selected), desc='Total', position=0, unit='call',
                 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]{postfix}')
    bars = {model: tqdm(total=len(cells), desc=f'  {model[:28]:28s}', position=i, unit='call',
                       bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}]{postfix}', leave=False)
            for i, (model, cells) in enumerate(jobs.items(), start=1)}
    lock, stop = Lock(), Event()

    def worker(model, cells):
        consecutive, errors = 0, 0
        with (output / 'logs' / f'{model}.jsonl').open('a') as log:
            def record(event, cell, **extra):
                log.write(json.dumps(redact({'time': timestamp(), 'event': event, 'cell': cell_key(cell), **extra})) + '\n')
                log.flush()

            for cell in cells:
                if stop.is_set():
                    return
                label = f"{cell['scenario']}|{cell['condition']}|r{cell['repetition']:03d}"
                bars[model].set_postfix_str(f'{label}|running|err={errors}')
                attempt = next_attempt(output / 'runs' / cell_key(cell), args.resume, args.retry_failed)
                if attempt is None:
                    raise RuntimeError('Attempt inventory changed after scheduling')
                record('running', cell, attempt=attempt.name)
                try:
                    data = load_inputs(cell['condition'], cell['scenario'], model)
                    status = execute_cell(plan, cell, attempt, args.trace_db, data, generate)
                except Exception as exc:
                    record('exception', cell, error=f'{type(exc).__name__}: {exc}')
                    raise
                record('finished', cell, status=status)
                failed = status['state'] != 'completed'
                errors += int(failed)
                consecutive = consecutive + 1 if failed else 0
                expected = len(data['task']['expected_files']) - int(data['seed_file'] is not None)
                present = expected - len(status.get('missing_generated_files', []))
                with lock:
                    summary['attempted'] += 1
                    summary['failed' if failed else 'completed'] += 1
                    bars[model].update(1)
                    bars[model].set_postfix_str(f"{label}|{present}/{expected}|err={errors}")
                    total.update(1)
                    total.set_postfix_str(f"err={summary['failed']}")
                    write_json(output / 'progress.json', summary)
                if consecutive >= args.max_consecutive_errors:
                    raise RuntimeError(f'Stopped after {consecutive} consecutive failures')

    pool = ThreadPoolExecutor(max_workers=workers)
    try:
        futures = {pool.submit(worker, model, cells): model for model, cells in jobs.items()}
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                model = futures[future]
                message = redact(f'{type(exc).__name__}: {exc}')
                with lock:
                    summary['aborted_models'][model] = message
                tqdm.write(f'MODEL ERROR ({model}): {message}')
    except KeyboardInterrupt:
        stop.set()
        summary['interrupted'] = True
        tqdm.write('Stopping new jobs; waiting for active calls to finish or time out before cleanup.')
        raise
    finally:
        # Keep the campaign lock until every worker has finished writing artifacts.
        pool.shutdown(wait=True, cancel_futures=True)
        for bar in bars.values():
            bar.close()
        total.close()
        summary['finished'] = timestamp()
        write_json(output / 'progress.json', redact(summary))
    print(f"Completed: {summary['completed']}, Failed: {summary['failed']}, Pre-skipped: {skipped}, Aborted models: {len(summary['aborted_models'])}")
    if summary['failed'] or summary['aborted_models'] or unresolved:
        raise RuntimeError('Campaign has failures; inspect logs before proceeding to another ablation')
    return summary

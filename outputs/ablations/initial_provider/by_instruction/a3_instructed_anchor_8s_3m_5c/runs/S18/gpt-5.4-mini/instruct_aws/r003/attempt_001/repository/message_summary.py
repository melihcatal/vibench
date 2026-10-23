def message_summary(results):
    total = len(results)
    ok = sum(1 for r in results if r.get("ok"))
    failed = total - ok
    return {"total": total, "ok": ok, "failed": failed}

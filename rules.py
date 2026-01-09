from models import ExecutionEvent

def check_policy(event: ExecutionEvent) -> str | None:
    """
    Very simple policy engine for v0.1
    """
    if event.status == "blocked":
        return f"Policy violation: step '{event.step}' is blocked."

    if event.status == "delayed":
        return f"Warning: step '{event.step}' is delayed."

    return None

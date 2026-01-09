from models import ExecutionEvent
from memory import MemoryStore
from rules import check_policy
from datetime import datetime

class ExecutionIntelligenceCore:
    def __init__(self):
        self.memory = MemoryStore()

    def process_event(self, event: ExecutionEvent) -> str:
        # Store event
        self.memory.save_event(event)

        # Policy reasoning
        policy_result = check_policy(event)

        # History reasoning
        past_count = self.memory.count_similar_events(
            process_id=event.process_id,
            step=event.step,
            status=event.status
        ) - 1

        history_note = ""
        if past_count > 0:
            history_note = (
                f" This issue has occurred {past_count} time(s) before, "
                "indicating a recurring pattern."
            )

        # Responsibility attribution
        owner = event.metadata.get("owner")
        responsibility_note = ""
        if owner:
            responsibility_note = f" Responsibility lies with '{owner}'."

        # Temporal reasoning
        first_seen, _ = self.memory.get_first_and_last_occurrence(
            process_id=event.process_id,
            step=event.step,
            status=event.status
        )

        temporal_note = ""
        if first_seen:
            duration = datetime.utcnow() - first_seen
            temporal_note = (
                f" This issue has been occurring for approximately "
                f"{duration.days} day(s)."
            )

        # 🔴 Risk scoring
        status_counts = self.memory.count_status_events(
            process_id=event.process_id,
            step=event.step
        )

        risk_level = "LOW RISK"
        if status_counts["blocked"] >= 3:
            risk_level = "HIGH RISK"
        elif status_counts["delayed"] >= 2:
            risk_level = "MEDIUM RISK"

        risk_note = f" Current risk level: {risk_level}."

        # Compose explanation
        if policy_result:
            return (
                f"Explanation: {policy_result}."
                f"{responsibility_note}"
                f"{history_note}"
                f"{temporal_note}"
                f"{risk_note}"
            )

        return (
            f"Execution OK: step '{event.step}' "
            f"for process '{event.process_id}' completed successfully."
            f"{responsibility_note}"
            f"{history_note}"
            f"{temporal_note}"
            f"{risk_note}"
        )
    
    def get_process_summary(self, process_id: str):
        events = self.memory.get_events_by_process(process_id)

        if not events:
            return None

        blocked_steps = set()
        responsible_teams = set()
        status_counts = {"blocked": 0, "delayed": 0, "completed": 0}

        for e in events:
            status_counts[e.status] = status_counts.get(e.status, 0) + 1
            if e.status == "blocked":
                blocked_steps.add(e.step)
            owner = e.metadata.get("owner")
            if owner:
                responsible_teams.add(owner)

        return {
            "process_id": process_id,
            "total_events": len(events),
            "status_counts": status_counts,
            "blocked_steps": list(blocked_steps),
            "responsible_teams": list(responsible_teams)
        }


    def get_process_risk(self, process_id: str):
        events = self.memory.get_events_by_process(process_id)

        if not events:
            return None

        blocked = sum(1 for e in events if e.status == "blocked")
        delayed = sum(1 for e in events if e.status == "delayed")

        risk = "LOW RISK"
        if blocked >= 3:
            risk = "HIGH RISK"
        elif delayed >= 2:
            risk = "MEDIUM RISK"

        return {
            "process_id": process_id,
            "blocked_count": blocked,
            "delayed_count": delayed,
            "risk_level": risk
        }


    def get_high_risk_processes(self):
        high_risk = []

        for pid in self.memory.get_all_process_ids():
            risk_info = self.get_process_risk(pid)
            if risk_info and risk_info["risk_level"] == "HIGH RISK":
                high_risk.append(risk_info)

        return high_risk

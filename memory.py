import os
import json
from typing import List
from datetime import datetime
from models import ExecutionEvent
from collections import defaultdict

class MemoryStore:
    def __init__(self, path: str = "memory.json"):
        self.path = path
        if not os.path.exists(self.path):
            self._write_empty()

    def _write_empty(self):
        with open(self.path, "w") as f:
            json.dump([], f)

    def save_event(self, event: ExecutionEvent):
        # Read safely
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
        except Exception:
            data = []

        # Serialize safely
        event_dict = event.dict()
        event_dict["timestamp"] = event_dict["timestamp"].isoformat()

        data.append(event_dict)

        # Write atomically
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def count_similar_events(
    self,
    process_id: str,
    step: str,
    status: str
    ) -> int:
        events = self.load_events()
        return sum(
            1
            for e in events
            if e.process_id == process_id
            and e.step == step
            and e.status == status
        )


    def load_events(self) -> List[ExecutionEvent]:
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
                return [ExecutionEvent(**e) for e in data]
        except Exception:
            return []
    from datetime import datetime

    def get_first_and_last_occurrence(
        self,
        process_id: str,
        step: str,
        status: str
    ):
        events = [
            e for e in self.load_events()
            if e.process_id == process_id
            and e.step == step
            and e.status == status
        ]

        if not events:
            return None, None

        events.sort(key=lambda e: e.timestamp)
        return events[0].timestamp, events[-1].timestamp

    def count_status_events(
        self,
        process_id: str,
        step: str
    ):
        events = [
            e for e in self.load_events()
            if e.process_id == process_id
            and e.step == step
        ]

        counts = {"blocked": 0, "delayed": 0}
        for e in events:
            if e.status in counts:
                counts[e.status] += 1

        return counts

    def get_events_by_process(self, process_id: str):
        return [
            e for e in self.load_events()
            if e.process_id == process_id
        ]

    def get_all_process_ids(self):
        return list({
            e.process_id for e in self.load_events()
        })


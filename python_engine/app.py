import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Railway Block Planning Engine")

# --- Data Models ---
class TrainRequest(BaseModel):
    train_id: str
    priority: int  # 1 (lowest) to 10 (highest, e.g., Rajdhani/Shatabdi)
    requested_duration_hours: int

class BlockPlanPayload(BaseModel):
    track_section_id: str
    total_available_hours: int
    trains: List[TrainRequest]

# --- Core Optimization Algorithm ---
def run_block_planning_algorithm(payload: BlockPlanPayload) -> dict:
    # Sort trains by highest priority first
    sorted_trains = sorted(payload.trains, key=lambda t: t.priority, reverse=True)
    
    allocated_schedule = []
    current_time_slot = 0  # Starting hour mark

    for train in sorted_trains:
        if current_time_slot + train.requested_duration_hours <= payload.total_available_hours:
            start_time = current_time_slot
            end_time = current_time_slot + train.requested_duration_hours
            current_time_slot = end_time

            allocated_schedule.append({
                "train_id": train.train_id,
                "priority": train.priority,
                "status": "APPROVED",
                "allocated_slot": f"{start_time:02d}:00 - {end_time:02d}:00"
            })
        else:
            allocated_schedule.append({
                "train_id": train.train_id,
                "priority": train.priority,
                "status": "REJECTED_NO_AVAILABLE_BLOCK",
                "allocated_slot": "N/A"
            })

    return {
        "track_section_id": payload.track_section_id,
        "total_trains_processed": len(payload.trains),
        "schedule": allocated_schedule
    }

# --- API Endpoints ---
@app.post("/api/v1/optimize")
def optimize_schedule(payload: BlockPlanPayload):
    return run_block_planning_algorithm(payload)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
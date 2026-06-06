from modelss.student import StudentCreate
from pathlib import Path
from datetime import datetime
import json
def write_log(action:str,student:StudentCreate):
    log_path=Path("logs")/"activity.json"
    log_path.parent.mkdir(exist_ok=True,parents=True)
    logs_info={
        "timestamp":datetime.now().isoformat(),
        "action":action,
        "student":student.model_dump()
    }
    logs=[]
    if log_path.exists():
        logs=json.loads(log_path.read_text(encoding="utf-8"))
    logs.append(logs_info)
    log_path.write_text(json.dumps(logs,indent=2,ensure_ascii=False))
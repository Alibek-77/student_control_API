from fastapi import Request,FastAPI,BackgroundTasks,HTTPException,status
import time,logging,json
from datetime import datetime
from pathlib import Path
todos = [
    {"id": 1, "title": "Выучить FastAPI", "done": False},
    {"id": 2, "title": "Написать API", "done": True},
]
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(),              
        logging.FileHandler("logs/app.log")   
    ]
)
app=FastAPI()
logger=logging.getLogger(__name__)
@app.middleware("http")
async def log_requests(request:Request,call_next):
    start_time=time.time()
    logger.info(f"{request.method}->{request.url}")
    response=await call_next(request)
    duration=time.time()-start_time
    logger.info(f"{response.status_code} in {duration:.3f}")
    return response
def write_log(action:str,title:str):
    log_path=Path("logs")/"todos.json"
    log_path.parent.mkdir(exist_ok=True,parents=True)
    log_entry={
        "timestamp":datetime.now().isoformat(),
        "action":action,
        "title":title
    }
    logs=[]
    if log_path.exists():
        logs=json.loads(log_path.read_text(encoding="utf-8"))
    logs.append(log_entry)
    log_path.write_text(json.dumps(logs,indent=2,ensure_ascii=False))
@app.get("/todos")
def get_todos():
    return todos
@app.post("/todos",status_code=201)
def create_todo(title:str,back_tasks:BackgroundTasks):
    id=max([t["id"] for t in todos])+1
    new_todo={"id":id,"title":title,"done":False}
    todos.append(new_todo)
    back_tasks.add_task(write_log,"created",title)
    return new_todo
@app.patch("/todos/{id}")
def done_todo(id:int,done:bool):
    for t in todos:
        if t["id"]==id:
            t["done"]=done
            return t
    logger.error("Todo not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Todos not found")

from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from routers import students,courses
from database import Base,engine
import os,logging,time
from dotenv import load_dotenv
load_dotenv()
allowed_origins=os.getenv("ALLOWED_ORIGINS","http://localhost:3000").split(",")
app=FastAPI(title="Student API",description="API for control students",version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"]
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),                    
        logging.FileHandler("logs/app.log")             
    ]
)
Base.metadata.create_all(bind=engine)
logger=logging.getLogger(__name__)
app.include_router(students.router)
app.include_router(courses.router)
@app.middleware("http")
async def log_requests(request:Request,call_next):
    start_time=time.time()
    logger.info(f"->{request.method} {request.url}")
    response=await call_next(request)
    duration=time.time()-start_time
    logger.info(f"{response.status_code} за {duration:.3f} sec")
    return response
@app.get("/",tags=["Health"])
def health_check():
    return {"status":"ok","version":"1.0.0"}

from fastapi import Header,HTTPException
from typing import Optional
from dotenv import load_dotenv
import os
load_dotenv()
def verify_api_key(api_key:Optional[str]=Header(None)):
    correct_key=os.getenv("API_KEY")
    if api_key is None:
        raise HTTPException(status_code=401,detail="Key not found!")
    if api_key!=correct_key:
        raise HTTPException(status_code=401,detail="Invalid API key")
    return api_key
def pagination(skip:int=0,limit:int=10):
    if limit>100:
        raise HTTPException(status_code=400,detail="Limit cannot exceed 100")
    return {"skip":skip,"limit":limit}

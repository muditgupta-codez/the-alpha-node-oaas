from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import subprocess
import json
import os

app = FastAPI(title="The Alpha Node OaaS API")

API_KEY = "alpha_node_secret_key_2026"
API_KEY_NAME = "X-Alpha-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate credentials")

class AuditRequest(BaseModel):
    url: str

@app.get("/")
async def root():
    return {"status": "online", "node": "The Alpha Node", "services": ["audit", "entropy", "health"]}

@app.post("/audit")
async def perform_audit(request: AuditRequest, key: str = Depends(get_api_key)):
    try:
        # Note: In a real prod environment, we'd use absolute paths
        result = subprocess.check_output(["python", "scripts/visual_audit.py", "--url", request.url], text=True)
        return json.loads(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/entropy")
async def generate_entropy(length: int = 32, count: int = 1, key: str = Depends(get_api_key)):
    try:
        result = subprocess.check_output(["python", "scripts/entropy_gen.py", "--length", str(length), "--count", str(count)], text=True)
        return json.loads(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def system_health(key: str = Depends(get_api_key)):
    try:
        result = subprocess.check_output(["python", "scripts/system_physician.py"], text=True)
        return json.loads(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

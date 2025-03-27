from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
async def home():
    return {'message': 'Hello world'}

def keep_alive():
    uvicorn.run(app, host='0.0.0.0', port=8080)
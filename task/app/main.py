import asyncio
import os

import uvicorn
from fastapi import FastAPI

from app import rabbitmq
from app.endpoints.task_router import task_router

app = FastAPI(title='Task Service')


@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume_tasks(loop))

app.include_router(task_router,prefix='/api')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))

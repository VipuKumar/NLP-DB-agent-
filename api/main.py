from fastapi import FastAPI
from api.routes.generate import router as generate_router
from api.routes.execute import router as execute_router

app=FastAPI(title="NLP DB Agent-V1")
app.include_router(generate_router)
app.include_router(execute_router)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.generate import router as generate_router
from api.routes.execute import router as execute_router




app=FastAPI(title="NLP DB Agent-V1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






app.include_router(generate_router)
app.include_router(execute_router)
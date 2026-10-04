from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.api import students, recruiters, admin

# Auto-create SQLite / PostgreSQL schema
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JobJugaad API",
    version="1.0",
    description="Placement ka Jugaad, AI ke Saath - BPUT Hackathon 2026"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(recruiters.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {
        "status": "online",
        "system": "JobJugaad Placement Intelligence",
        "docs": "/docs"
    }
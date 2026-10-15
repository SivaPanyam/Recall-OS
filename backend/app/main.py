from fastapi import FastAPI

app = FastAPI(
    title="OES - Personal AI Memory Engine",
    description="A local-first AI system for remembering your learning journey.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to OES",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "oes-backend",
        "version": "0.1.0",
    }

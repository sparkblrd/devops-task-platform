"""HTTP application entry point."""

from fastapi import FastAPI

from app.routers.tasks import router as tasks_router

app = FastAPI(
    title="DevOps Task Platform",
    description="A small REST API for a hands-on DevOps portfolio project.",
    version="0.1.0",
)

app.include_router(tasks_router)


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    """Provide basic service information."""
    return {"service": "devops-task-platform", "version": "0.1.0"}


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Liveness check: the application is running."""
    return {"status": "ok"}

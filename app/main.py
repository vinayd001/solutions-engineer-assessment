from fastapi import FastAPI


def create_app() -> FastAPI:
    """Application factory for tests and ASGI servers."""
    app = FastAPI(
        title="Partner Events API",
        description="Payment lifecycle ingestion and reconciliation.",
        version="0.1.0",
    )

    @app.get("/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app

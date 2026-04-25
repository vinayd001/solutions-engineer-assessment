from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

DEFAULT_DATABASE_URL = "sqlite:///./app.db"


def get_database_url() -> str:
    return os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)


def get_engine() -> Engine:
    url = get_database_url()
    kwargs: dict = {"future": True}
    if url.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}
    return create_engine(url, **kwargs)

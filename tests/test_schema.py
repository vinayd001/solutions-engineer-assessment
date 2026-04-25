from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect


def test_alembic_upgrade_creates_core_tables(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "migration.db"
    url = f"sqlite:///{db_path}"
    monkeypatch.setenv("DATABASE_URL", url)

    root = Path(__file__).resolve().parents[1]
    cfg = Config(str(root / "alembic.ini"))
    command.upgrade(cfg, "head")

    engine = create_engine(url)
    insp = inspect(engine)
    assert insp.has_table("merchants")
    assert insp.has_table("transactions")
    assert insp.has_table("events")

    uqs = insp.get_unique_constraints("events")
    assert any("event_id" in uq.get("column_names", ()) for uq in uqs)

    idx_names = {ix["name"] for ix in insp.get_indexes("transactions")}
    assert "ix_transactions_merchant_updated" in idx_names
    assert "ix_transactions_merchant_payment" in idx_names

    ev_idx = {ix["name"] for ix in insp.get_indexes("events")}
    assert "ix_events_transaction_occurred" in ev_idx

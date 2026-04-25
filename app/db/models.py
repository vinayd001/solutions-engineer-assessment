from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from sqlalchemy import JSON, DateTime, ForeignKey, Index, Numeric, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Merchant(Base):
    __tablename__ = "merchants"

    merchant_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    transactions: Mapped[list["Transaction"]] = relationship(back_populates="merchant")


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        Index("ix_transactions_merchant_updated", "merchant_id", "updated_at"),
        Index("ix_transactions_merchant_payment", "merchant_id", "payment_status"),
    )

    transaction_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    merchant_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("merchants.merchant_id", ondelete="RESTRICT"), nullable=False
    )
    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(19, 4), nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    payment_status: Mapped[str] = mapped_column(
        String(32), nullable=False, server_default=text("'none'")
    )
    settlement_status: Mapped[str] = mapped_column(
        String(32), nullable=False, server_default=text("'none'")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    last_event_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    merchant: Mapped["Merchant"] = relationship(back_populates="transactions")
    events: Mapped[list["Event"]] = relationship(
        back_populates="transaction",
        order_by="Event.occurred_at",
    )


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (Index("ix_events_transaction_occurred", "transaction_id", "occurred_at"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    transaction_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("transactions.transaction_id", ondelete="CASCADE"),
        nullable=False,
    )
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(19, 4), nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    raw_payload: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)

    transaction: Mapped["Transaction"] = relationship(back_populates="events")

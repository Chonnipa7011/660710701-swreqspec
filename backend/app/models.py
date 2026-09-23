from datetime import date, datetime, time
from enum import Enum
from typing import Optional
from uuid import UUID

from sqlalchemy import Date, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Time, UniqueConstraint
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED_NOTIFICATION = "failed_notification"
    EXPIRED = "expired"


class NotificationChannel(str, Enum):
    SMS = "SMS"
    LINE = "LINE"


class NotificationStatus(str, Enum):
    QUEUED = "queued"
    SENT = "sent"
    FAILED = "failed"


class Booking(Base):
    """Booking record; supports FR-BKG-02, FR-BKG-04, FR-BKG-05, FR-BKG-06 and IF-HIS-01."""

    __tablename__ = "booking"
    __table_args__ = (
        UniqueConstraint("patient_hn", "booking_date", name="uq_booking_patient_date"),
    )

    booking_id: Mapped[UUID] = mapped_column(CHAR(36), primary_key=True)
    patient_hn: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    booking_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    slot_start: Mapped[time] = mapped_column(Time, nullable=False)
    slot_end: Mapped[time] = mapped_column(Time, nullable=False)
    package_id: Mapped[str] = mapped_column(String(50), nullable=False)
    queue_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[BookingStatus] = mapped_column(
        SqlEnum(BookingStatus), nullable=False, default=BookingStatus.PENDING
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    source_user_id: Mapped[str] = mapped_column(String(100), nullable=False)


class SlotCapacity(Base):
    """Slot capacity record; supports FR-BKG-01, FR-BKG-03 and FR-BKG-04."""

    __tablename__ = "slot_capacity"
    __table_args__ = (
        UniqueConstraint("slot_date", "slot_start", "slot_end", name="uq_slot_capacity_period"),
    )

    slot_date: Mapped[date] = mapped_column(Date, primary_key=True)
    slot_start: Mapped[time] = mapped_column(Time, primary_key=True)
    slot_end: Mapped[time] = mapped_column(Time, primary_key=True)
    quota: Mapped[int] = mapped_column(Integer, nullable=False)
    used_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_available: Mapped[bool] = mapped_column(nullable=False, default=True, index=True)


class NotificationLog(Base):
    """Notification record; supports FR-BKG-05 and IF-NOT-01."""

    __tablename__ = "notification_log"

    notification_id: Mapped[UUID] = mapped_column(CHAR(36), primary_key=True)
    booking_id: Mapped[UUID] = mapped_column(
        CHAR(36), ForeignKey("booking.booking_id"), nullable=False, index=True
    )
    channel: Mapped[NotificationChannel] = mapped_column(SqlEnum(NotificationChannel), nullable=False)
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[NotificationStatus] = mapped_column(
        SqlEnum(NotificationStatus), nullable=False, default=NotificationStatus.QUEUED
    )
    next_retry_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, index=True)


class AccessAuditLog(Base):
    """Health-data access audit record; supports DOM-PDPA-01."""

    __tablename__ = "access_audit_log"

    log_id: Mapped[UUID] = mapped_column(CHAR(36), primary_key=True)
    accessed_by: Mapped[str] = mapped_column(String(100), nullable=False)
    accessed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    patient_hn: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
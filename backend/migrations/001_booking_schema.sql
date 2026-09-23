CREATE TABLE booking (
    booking_id CHAR(36) NOT NULL,
    patient_hn VARCHAR(50) NOT NULL,
    booking_date DATE NOT NULL,
    slot_start TIME NOT NULL,
    slot_end TIME NOT NULL,
    package_id VARCHAR(50) NOT NULL,
    queue_number INT NULL,
    status ENUM('pending', 'confirmed', 'failed_notification', 'expired') NOT NULL DEFAULT 'pending',
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    source_user_id VARCHAR(100) NOT NULL,
    PRIMARY KEY (booking_id),
    UNIQUE KEY uq_booking_patient_date (patient_hn, booking_date),
    KEY ix_booking_patient_hn (patient_hn),
    KEY ix_booking_date (booking_date)
);

CREATE TABLE slot_capacity (
    slot_date DATE NOT NULL,
    slot_start TIME NOT NULL,
    slot_end TIME NOT NULL,
    quota INT NOT NULL,
    used_count INT NOT NULL DEFAULT 0,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (slot_date, slot_start, slot_end),
    UNIQUE KEY uq_slot_capacity_period (slot_date, slot_start, slot_end),
    KEY ix_slot_capacity_available (is_available)
);

CREATE TABLE notification_log (
    notification_id CHAR(36) NOT NULL,
    booking_id CHAR(36) NOT NULL,
    channel ENUM('SMS', 'LINE') NOT NULL,
    attempt_count INT NOT NULL DEFAULT 0,
    status ENUM('queued', 'sent', 'failed') NOT NULL DEFAULT 'queued',
    next_retry_at DATETIME NULL,
    PRIMARY KEY (notification_id),
    KEY ix_notification_booking_id (booking_id),
    KEY ix_notification_next_retry_at (next_retry_at),
    CONSTRAINT fk_notification_booking FOREIGN KEY (booking_id) REFERENCES booking (booking_id)
);

CREATE TABLE access_audit_log (
    log_id CHAR(36) NOT NULL,
    accessed_by VARCHAR(100) NOT NULL,
    accessed_at DATETIME NOT NULL,
    patient_hn VARCHAR(50) NOT NULL,
    action VARCHAR(100) NOT NULL,
    PRIMARY KEY (log_id),
    KEY ix_access_audit_accessed_at (accessed_at),
    KEY ix_access_audit_patient_hn (patient_hn)
);
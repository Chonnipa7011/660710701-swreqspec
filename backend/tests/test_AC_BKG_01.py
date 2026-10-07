# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from tests.conftest import AUTH


def test_AC_BKG_01(client, make_slot):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง จองแล้วต้องสำเร็จ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201


def test_TC_BKG_01_1_last_seat(client, db, make_slot):
    from app.db.models import Booking

    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจองช่วง 09.00 น.
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกสำเร็จ; มีการจอง 1 รายการ; ที่นั่งว่างเป็น 0; แสดงหมายเลขคิว (รอ Q-02)
    assert res.status_code == 201
    assert db.query(Booking).filter_by(slot_id=slot.id).count() == 1
    db.refresh(slot)
    assert slot.remaining == 0
    # ยังไม่ตรวจการแสดงหมายเลขคิว เพราะรอ Q-02


def test_TC_BKG_01_2_no_seat_left(client, db, make_slot):
    from app.db.models import Booking

    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. เหลือ 0 ที่ (มีคนจองที่สุดท้ายไปแล้ว)
    slot = make_slot(start="09:00", remaining=0)
    initial_booking_count = db.query(Booking).count()

    # When: ยืนยันการจองช่วง 09.00 น.
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: ปฏิเสธ ตอบ 409; ไม่มีการจองใหม่; ที่นั่งว่างยังเป็น 0 ไม่ติดลบ
    assert res.status_code == 409
    assert db.query(Booking).count() == initial_booking_count
    db.refresh(slot)
    assert slot.remaining == 0


def test_TC_BKG_01_3_not_authenticated(client, db, make_slot):
    from app.db.models import Booking

    # Given: ยังไม่ได้ยืนยันตัวตน และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)
    initial_booking_count = db.query(Booking).count()

    # When: ยืนยันการจองช่วง 09.00 น.
    res = client.post("/bookings", json={"slot_id": slot.id})

    # Then: ปฏิเสธ ตอบ 401; ไม่มีการจอง; ที่นั่งว่างยังเป็น 1
    assert res.status_code == 401
    assert db.query(Booking).count() == initial_booking_count
    db.refresh(slot)
    assert slot.remaining == 1

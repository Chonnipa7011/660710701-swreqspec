# AC-BKG-02 (FR-BKG-02)
from app.auth.idp import get_verified_hn
from app.db.models import Booking
from tests.conftest import AUTH


def test_TC_BKG_02_1_same_day_duplicate_rejected(client, db, make_slot):
    # Given: ยืนยันตัวตนแล้ว และมีคิวที่ยังไม่ได้ใช้ของผู้รับบริการคนเดิมในวันเดียวกัน
    hn = get_verified_hn(AUTH["Authorization"])
    existing_slot = make_slot(start="08:00", remaining=0)
    existing_booking = Booking(
        hn=hn,
        slot_id=existing_slot.id,
        booking_date=existing_slot.slot_date,
        queue_no=None,
        status="BOOKED",
    )
    db.add(existing_booking)
    db.commit()
    db.refresh(existing_booking)
    new_slot = make_slot(start="09:00", remaining=1)
    initial_booking_count = db.query(Booking).count()

    # When: จองคิวใหม่ในวันเดียวกัน
    response = client.post("/bookings", json={"slot_id": new_slot.id}, headers=AUTH)

    # Then: ปฏิเสธการจองใหม่; ส่ง booking เดิมกลับ; แสดงหมายเลขคิวเดิม (รอ Q-02)
    assert response.status_code != 201
    assert db.query(Booking).count() == initial_booking_count
    assert response.json()["booking_id"] == existing_booking.id
    # ยังไม่ตรวจการแสดงหมายเลขคิวเดิม เพราะรอ Q-02


def test_TC_BKG_02_2_previous_day_booking_allowed(client, db, make_slot):
    # Given: ยืนยันตัวตนแล้ว และมีคิวที่ยังไม่ได้ใช้ของผู้รับบริการคนเดิมในวันก่อนหน้าวันที่เลือก;
    # ช่วงวันที่เลือกมีที่นั่งว่าง 1 ที่
    hn = get_verified_hn(AUTH["Authorization"])
    previous_slot = make_slot(start="08:00", remaining=0, days_from_today=1)
    db.add(
        Booking(
            hn=hn,
            slot_id=previous_slot.id,
            booking_date=previous_slot.slot_date,
            queue_no=None,
            status="BOOKED",
        )
    )
    db.commit()
    selected_slot = make_slot(start="09:00", remaining=1, days_from_today=2)

    # When: จองคิวในวันที่ถัดจากคิวเดิม
    response = client.post("/bookings", json={"slot_id": selected_slot.id}, headers=AUTH)

    # Then: ยอมรับการจอง; บันทึกการจองใหม่สำหรับวันที่เลือก; ที่นั่งว่างของช่วงที่เลือกเป็น 0
    assert response.status_code == 201
    assert db.query(Booking).filter_by(slot_id=selected_slot.id).count() == 1
    db.refresh(selected_slot)
    assert selected_slot.remaining == 0


def test_TC_BKG_02_3_other_person_same_day_allowed(client, db, make_slot):
    # Given: ยืนยันตัวตนแล้ว; ผู้รับบริการคนอื่นมีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน;
    # ผู้ใช้ปัจจุบันไม่มีคิวในวันนั้น; ช่วงที่เลือกมีที่นั่งว่าง 1 ที่
    other_person_slot = make_slot(start="08:00", remaining=0)
    db.add(
        Booking(
            hn="OTHER-HN",
            slot_id=other_person_slot.id,
            booking_date=other_person_slot.slot_date,
            queue_no=None,
            status="BOOKED",
        )
    )
    db.commit()
    selected_slot = make_slot(start="09:00", remaining=1)

    # When: จองคิวในวันเดียวกัน
    response = client.post("/bookings", json={"slot_id": selected_slot.id}, headers=AUTH)

    # Then: ยอมรับการจองของผู้ใช้ปัจจุบัน; บันทึกการจองใหม่; ที่นั่งว่างของช่วงที่เลือกเป็น 0
    assert response.status_code == 201
    assert db.query(Booking).filter_by(slot_id=selected_slot.id).count() == 1
    db.refresh(selected_slot)
    assert selected_slot.remaining == 0

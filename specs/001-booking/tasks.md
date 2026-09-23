# Tasks: จองคิวตรวจสุขภาพ (Booking)

- Feature: จองคิวตรวจสุขภาพ
- Spec ID: SPEC-BKG-001
- อ้างอิง: `specs/001-booking/plan.md`
- วันที่: 2569-09-23
- สรุป: มีทั้งหมด 15 tasks สำหรับ schema, backend API, หน้าจอ, การเชื่อมต่อ และการทดสอบตาม acceptance criteria
- มี 2 tasks ที่ต้องรอคำตอบจาก Open Questions คือ Q-01 และ Q-02

## รายการ task

### T-01 สร้าง schema ข้อมูลการจอง
- รองรับ: FR-BKG-01, FR-BKG-02, FR-BKG-04, FR-BKG-05, FR-BKG-06, CON-TECH-01, IF-HIS-01, DOM-PDPA-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03, T-04, T-05, T-07 และ T-14
- ไฟล์ที่แตะ: `backend/app/models.py`, `backend/app/db.py`, `backend/migrations/`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: มี schema ของ `booking`, `slot_capacity`, `notification_log` และ `access_audit_log` บน MySQL และตาราง `booking` ไม่มีเลขบัตรประชาชน
- สถานะ: เสร็จ รอทีมตรวจ

### T-02 เชื่อมผลยืนยันตัวตนและข้อมูลผู้รับบริการ
- รองรับ: IF-IDP-01, IF-HIS-01, NFR-SEC-01, DOM-PDPA-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03, T-04, T-05 และ T-14
- ไฟล์ที่แตะ: `backend/app/auth.py`, `backend/app/integrations/his.py`, `backend/app/dependencies.py`, `backend/requirements.txt`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: API ที่เข้าถึงข้อมูลผู้รับบริการรับเฉพาะ session ที่ยืนยันจาก IDP ใช้ HN จาก HIS และตั้งค่าการรับส่งผ่าน TLS 1.2 ขึ้นไปตามสภาพแวดล้อมที่ทีมเลือก
- สถานะ: พร้อมทำ

### T-03 สร้าง API ค้นหาช่วงเวลาว่าง
- รองรับ: FR-BKG-01, FR-BKG-06, CON-TECH-01, IF-IDP-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-09 และ T-13
- ไฟล์ที่แตะ: `backend/app/routers/booking.py`, `backend/app/services/slot_service.py`, `backend/tests/test_slots_api.py`
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: `GET /api/booking/slots` คืนช่วงเวลาภายใน 30 วันพร้อมจำนวนที่นั่งคงเหลือ และคำนวณใหม่เมื่อรับแพ็กเกจต่างกัน
- สถานะ: พร้อมทำ

### T-04 สร้าง API ตรวจคิวซ้ำรายวัน
- รองรับ: FR-BKG-02, IF-IDP-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-12
- ไฟล์ที่แตะ: `backend/app/routers/booking.py`, `backend/app/services/duplicate_service.py`, `backend/tests/test_duplicate_api.py`
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: `POST /api/booking/check-duplicate` ตรวจคิวที่ยังไม่ได้ใช้ของ HN ในวันเดียวกันและคืนหมายเลขคิวเดิมเมื่อพบ
- สถานะ: พร้อมทำ

### T-05 สร้าง flow ยืนยันการจองแบบ atomic
- รองรับ: FR-BKG-04, CON-TECH-01, IF-IDP-01, IF-HIS-01
- ตรวจด้วย: AC-BKG-01
- ไฟล์ที่แตะ: `backend/app/routers/booking.py`, `backend/app/services/booking_service.py`, `backend/tests/test_AC_BKG_01_success_booking_and_slot_reduction.py`
- ต้องทำหลัง: T-01, T-02, T-04
- เสร็จเมื่อ: `test_AC_BKG_01_success_booking_and_slot_reduction` ผ่าน โดยบันทึกการจอง ตัดที่นั่งเหลือ 0 และแสดงหมายเลขคิวตามกติกาที่ทีมตอบ Q-02 แล้ว
- สถานะ: รอ Q-02

### T-06 จัดการช่วงเวลาเต็มและตัวเลือกใกล้เคียง
- รองรับ: FR-BKG-03, CON-TECH-01
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: `backend/app/services/booking_service.py`, `backend/app/services/slot_service.py`, `backend/tests/test_AC_BKG_03_slot_full_offer_alternatives.py`
- ต้องทำหลัง: T-03, T-05
- เสร็จเมื่อ: `test_AC_BKG_03_slot_full_offer_alternatives` ผ่าน โดยแจ้ง “ช่วงเวลาเต็ม” คืนตัวเลือกใกล้เคียง 3 รายการ และไม่สร้างการจองซ้อนตามขอบเขตที่ทีมตอบ Q-01 แล้ว
- สถานะ: รอ Q-01

### T-07 สร้างคิวแจ้งเตือนแบบ asynchronous และ retry
- รองรับ: FR-BKG-05, IF-NOT-01, NFR-REL-02
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: `backend/app/services/notification_service.py`, `backend/app/workers/notification_worker.py`, `backend/app/routers/notification.py`, `backend/tests/test_AC_BKG_04_booking_persists_when_notification_fails.py`
- ต้องทำหลัง: T-01, T-05
- เสร็จเมื่อ: `test_AC_BKG_04_booking_persists_when_notification_fails` ผ่าน โดยบันทึกการจอง แสดงหมายเลขคิว และสร้าง retry ภายใน 5 นาทีโดยไม่รอผลส่งข้อความ
- สถานะ: พร้อมทำ

### T-08 สร้าง API ดูสถานะการจอง
- รองรับ: FR-BKG-05, IF-IDP-01, IF-HIS-01, DOM-PDPA-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-10 และ T-14
- ไฟล์ที่แตะ: `backend/app/routers/booking.py`, `backend/app/services/booking_service.py`, `backend/tests/test_booking_status_api.py`
- ต้องทำหลัง: T-01, T-02, T-05, T-07
- เสร็จเมื่อ: `GET /api/booking/{bookingId}/status` คืนสถานะและหมายเลขคิวของผู้รับบริการที่ผ่านการยืนยัน พร้อมบันทึก audit log
- สถานะ: พร้อมทำ

### T-09 สร้างหน้าจอเลือกแพ็กเกจ วัน และช่วงเวลา
- รองรับ: FR-BKG-01, FR-BKG-06, ASM-04
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-11
- ไฟล์ที่แตะ: `frontend/src/pages/BookingPage.jsx`, `frontend/src/api/client.js`, `frontend/src/__tests__/BookingPage.test.jsx`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: หน้าจอใช้ API จำลองตามสัญญาใน plan แสดงช่วงเวลาภายใน 30 วัน จำนวนที่นั่ง ช่วงเต็มเป็นสีเทาและกดไม่ได้ และคำนวณรายการใหม่เมื่อเปลี่ยนแพ็กเกจ
- สถานะ: พร้อมทำ

### T-10 สร้างหน้าจอผลยืนยันและหมายเลขคิว
- รองรับ: FR-BKG-04, FR-BKG-05
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-11
- ไฟล์ที่แตะ: `frontend/src/pages/BookingConfirmationPage.jsx`, `frontend/src/__tests__/BookingConfirmationPage.test.jsx`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: หน้าจอจำลองแสดงผลสำเร็จหรือการแจ้งเตือนไม่สำเร็จพร้อมหมายเลขคิวและสถานะที่ API คืนมา
- สถานะ: พร้อมทำ

### T-11 ต่อหน้าจอกับ API จริง
- รองรับ: FR-BKG-01, FR-BKG-02, FR-BKG-03, FR-BKG-04, FR-BKG-05, FR-BKG-06, IF-IDP-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานเชื่อมต่อของ T-09 และ T-10 กับ T-03, T-04, T-05, T-06, T-07 และ T-08
- ไฟล์ที่แตะ: `frontend/src/api/client.js`, `frontend/src/App.jsx`, `frontend/src/pages/BookingPage.jsx`, `frontend/src/pages/BookingConfirmationPage.jsx`, `frontend/src/__tests__/booking-flow.integration.test.jsx`
- ต้องทำหลัง: T-03, T-04, T-05, T-06, T-07, T-08, T-09, T-10
- เสร็จเมื่อ: `booking-flow.integration.test.jsx` ผ่านโดยหน้าจอเรียก API จริงตามสัญญา plan และแสดงผลของ flow หลักกับ exception ได้
- สถานะ: พร้อมทำ

### T-12 ทดสอบการป้องกันจองซ้ำ
- รองรับ: FR-BKG-02
- ตรวจด้วย: AC-BKG-02
- ไฟล์ที่แตะ: `backend/tests/test_AC_BKG_02_reject_same_day_active_booking.py`
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: `test_AC_BKG_02_reject_same_day_active_booking` ผ่าน โดยปฏิเสธการจองใหม่และแสดงหมายเลขคิวเดิม
- สถานะ: พร้อมทำ

### T-13 ทดสอบประสิทธิภาพการค้นหาช่วงเวลา
- รองรับ: FR-BKG-01, NFR-PERF-01
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: `backend/tests/performance/test_AC_BKG_05_slot_lookup_p95_under_2s.py`, `docs/srs/`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: `test_AC_BKG_05_slot_lookup_p95_under_2s` รันด้วยผู้ใช้จำลอง 200 คนและวัด p95 ได้ไม่เกิน 2 วินาที หรือมีผลการทดสอบบันทึกไว้ให้ทีมพิจารณา
- สถานะ: พร้อมทำ

### T-14 ทดสอบ audit log การเข้าถึงข้อมูล
- รองรับ: DOM-PDPA-01, IF-IDP-01, IF-HIS-01
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: `backend/tests/test_AC_BKG_06_audit_log_written.py`, `backend/app/services/audit_service.py`
- ต้องทำหลัง: T-02, T-05, T-08
- เสร็จเมื่อ: `test_AC_BKG_06_audit_log_written` ผ่านและ audit log ระบุผู้เข้าถึง เวลา และ HN ของผู้รับบริการ
- สถานะ: พร้อมทำ

### T-15 ทดสอบ usability ตามเวลาการจอง
- รองรับ: NFR-USE-01, FR-BKG-01, FR-BKG-04
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นการตรวจ NFR-USE-01
- ไฟล์ที่แตะ: `frontend/src/__tests__/usability-booking.test.jsx`, `docs/srs/`
- ต้องทำหลัง: T-11
- เสร็จเมื่อ: มีการทดสอบผู้ใช้ใหม่ 10 คนและบันทึกว่าผู้ใช้ 8 คนขึ้นไปจองสำเร็จภายใน 3 นาทีโดยไม่ขอความช่วยเหลือ
- สถานะ: พร้อมทำ

## ตารางตรวจความครบของ Acceptance Criteria

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-BKG-01 | T-05 |
| AC-BKG-02 | T-12 |
| AC-BKG-03 | T-06 |
| AC-BKG-04 | T-07 |
| AC-BKG-05 | T-13 |
| AC-BKG-06 | T-14 |

## ตารางตรวจความครบของ Constraints

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-TECH-01 | T-01, T-05, T-06 |
| DOM-PDPA-01 | T-01, T-02, T-08, T-14 |
| IF-IDP-01 | T-02, T-03, T-04, T-05, T-08, T-11, T-14 |
| IF-HIS-01 | T-01, T-02, T-04, T-08, T-14 |
| IF-NOT-01 | T-07 |

## สิ่งที่ยังไม่ทำ

- Q-01: “ช่วงเวลาใกล้เคียง” นับเฉพาะวันเดียวกัน หรือรวมวันถัดไปด้วย? งานที่รอ: T-06
- Q-02: หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง? งานที่รอ: T-05

# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md Draft v3 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-07 08.57 | test: 10 ผ่าน 0 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 (ตรวจเวลา ไม่ได้ตรวจช่วง 30 วัน) | T-02 เสร็จ | `backend/app/slots/router.py:get_slots`; `backend/app/slots/service.py:list_available_slots` | `test_AC_BKG_05` ผ่าน แต่ทดสอบแบบเรียกต่อเนื่อง ไม่ใช่ผู้ใช้พร้อมกัน 200 คน | ช่องโหว่: F-09 |
| FR-BKG-02 | AC-BKG-02 | T-04 เสร็จ | `backend/app/booking/service.py:create_booking`; `backend/app/booking/router.py:create_booking` | `test_TC_BKG_02_1_same_day_duplicate_rejected`, `test_TC_BKG_02_2_previous_day_booking_allowed`, `test_TC_BKG_02_3_other_person_same_day_allowed` ผ่าน; การตรวจหมายเลขคิวเดิมรอ Q-02 | รอ Q-02 |
| FR-BKG-03 | AC-BKG-03 | T-05 พร้อมทำ; T-11/T-12 พร้อมทำ | มีเพียงการปฏิเสธช่วงเต็มใน `backend/app/booking/router.py:create_booking`; ยังไม่มีช่วงเวลาใกล้เคียง | ไม่มี | ยังไม่ถึง |
| FR-BKG-04 | AC-BKG-01 | T-03 เสร็จ; T-06 รอ Q-02; การส่งข้อความยังไม่ทำใน T-07 | `backend/app/booking/service.py:create_booking`; `backend/app/booking/router.py:create_booking` | `test_TC_BKG_01_1_last_seat`, `test_TC_BKG_01_2_no_seat_left`, `test_TC_BKG_01_3_not_authenticated` ผ่าน; การแสดงคิวรอ Q-02; test เดิม `test_AC_BKG_01` ตรวจเพียง status 201 | ยังไม่ถึง: การส่งข้อความ T-07; รอ Q-02: การออก/แสดงเลขคิว |
| FR-BKG-05 | AC-BKG-04 | T-07 พร้อมทำ | ไม่มี notify queue หรือ `GET /bookings/{id}` ใน `backend/app/` | ไม่มี | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC ที่ตรวจการเปลี่ยนแพ็กเกจ | T-02 เสร็จ (ตัวกรอง API); T-10/T-12 พร้อมทำ (หน้าจอ) | `backend/app/slots/service.py:list_available_slots` กรอง `package_code`; หน้าจอเลือกแพ็กเกจยังไม่มี | ไม่มี test เปลี่ยนแพ็กเกจ | ช่องโหว่: F-07 |
| NFR-PERF-01 | AC-BKG-05 | T-02 เสร็จ | `backend/app/slots/router.py:get_slots`; `backend/app/slots/service.py:list_available_slots` | `test_AC_BKG_05` ผ่านที่ p95 <= 2 วินาที แต่ไม่ได้จำลอง concurrent users 200 คน | ช่องโหว่: F-05 |
| NFR-SEC-01 | ไม่มี AC เฉพาะ | ไม่มี task เฉพาะ | ต้องยืนยัน TLS 1.2+ ที่ deployment/runtime | ไม่มี test TLS ใน repo | ยังไม่ถึง: ยืนยันที่ deployment |
| NFR-REL-02 | AC-BKG-04 | T-07 พร้อมทำ | ยังไม่มีคิวหรือการ retry | ไม่มี | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC เฉพาะ | T-10 ถึง T-12 ยังพร้อมทำ; ไม่มี task ทดสอบผู้ใช้ 8 ใน 10 คน | หน้าจอ `frontend/src/App.jsx` ยังเป็นโครงเริ่มต้น | ไม่มี user test | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC เฉพาะ | T-01 เสร็จ | `backend/app/config.py:DATABASE_URL`; `backend/app/db/session.py` ใช้ URL ที่กำหนด | `test_T01_tables_created`, `test_T01_no_national_id` ผ่านบน SQLite; ยังไม่มีผลทดสอบ PostgreSQL | ยังไม่ถึง: ยังยืนยันการทำงานกับ PostgreSQL ไม่ได้ |
| DOM-PDPA-01 | AC-BKG-06 | T-08 พร้อมทำ | มี schema `AuditLog` ใน `backend/app/db/models.py`; ไม่พบ middleware หรือการเขียน audit log | `test_T01_tables_created` ตรวจเพียงการมีตาราง; ไม่มี test บันทึกการเข้าถึง | ยังไม่ถึง |
| IF-IDP-01 | AC-BKG-01 ใช้ token จำลองใน happy path; AC-BKG-01 TC-3 ตรวจ 401 | T-03 เสร็จ | `backend/app/auth/idp.py:get_verified_hn` ตรวจเพียง prefix ของ Authorization ไม่ติดต่อระบบ IDP | `test_TC_BKG_01_3_not_authenticated` ผ่าน; ไม่มี test ยืนยันผลจาก IDP จริง | ช่องโหว่: F-02 |
| IF-HIS-01 | ไม่มี AC เฉพาะ | T-01 เสร็จ; T-09 พร้อมทำ | `Booking` เก็บ HN และไม่มีคอลัมน์ national_id; ไม่พบ HIS lookup; request booking ไม่รับเลขบัตรประชาชน | `test_T01_no_national_id` ผ่านเฉพาะการไม่มีคอลัมน์; ไม่มี test HIS lookup | ยังไม่ถึง |
| IF-NOT-01 | AC-BKG-04 ทางอ้อม | T-07 พร้อมทำ | ไม่พบการส่งข้อความแบบ asynchronous | ไม่มี | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| `backend/app/main.py:lifespan`, `app` | CON-TECH-01 | บางส่วน | สร้างตารางตอนเริ่มระบบและรวม router; ยังไม่ยืนยันการเชื่อม PostgreSQL |
| `GET /slots` — `backend/app/slots/router.py:get_slots` | FR-BKG-01, FR-BKG-06 | ไม่ครบ | คืนวัน/เวลา/remaining และรับ package_code; จำกัดวันเป็น 30 วันตาม FR-BKG-01 แต่ไม่มี AC ตรวจ package change หรือขอบวัน 30 วัน |
| `backend/app/slots/service.py:list_available_slots` | FR-BKG-01, FR-BKG-06, ASM-01 | บางส่วน | กรองแพ็กเกจและ remaining > 0; DAYS_AHEAD=30; ยังไม่มี AC/test ยืนยัน package change หรือขอบเขตวัน |
| `POST /bookings` — `backend/app/booking/router.py:create_booking` | FR-BKG-02, FR-BKG-03, FR-BKG-04, IF-IDP-01, IF-HIS-01 | ไม่ครบ | ปฏิเสธ booking ซ้ำของ HN เดิมในวันเดียวกันและคืน booking เดิม; ยังไม่มีเสนอช่วงเวลาใกล้เคียง/ส่ง notification; ไม่รับหรือ log national_id; auth เป็น prefix mock |
| `BookingRequest.slot_id`; response `booking_id`, `slot_id`, `queue_no` | FR-BKG-02, FR-BKG-04, Q-02 | บางส่วน | slot_id สอดคล้องกับ API plan; duplicate response คืน booking_id/slot_id เดิม; queue_no เป็น null ระหว่างรอ Q-02 |
| `backend/app/booking/service.py:create_booking` | FR-BKG-02, FR-BKG-04 | บางส่วน | ปฏิเสธเมื่อมี status BOOKED ของ HN เดิมในวันเดียวกัน; ปฏิเสธเมื่อ remaining <= 0, ลดที่นั่งและบันทึก booking; queue_no ยังว่างรอ Q-02; ยังไม่ส่งคำขอแจ้งเตือน |
| `backend/app/auth/idp.py:get_verified_hn` | IF-IDP-01 | ไม่ครบ | เช็คเพียง token prefix จำลอง ไม่ได้รับผลยืนยันตัวตนจากระบบ IDP |
| `backend/app/db/models.py:Slot`, `Booking`, `AuditLog` | FR-BKG-01/02/04/06, IF-HIS-01, DOM-PDPA-01 | บางส่วน | schema มี slot/booking/audit; ไม่มี national_id ใน bookings; queue_no ยังใช้รูปแบบที่ยังรอ Q-02 |
| `backend/app/config.py:DATABASE_URL`, `backend/app/db/session.py:get_db` | CON-TECH-01 | ยังยืนยันไม่ได้ | ใช้ DATABASE_URL ได้ แต่ default เป็น SQLite และชุดทดสอบใช้ SQLite; ไม่มีผลยืนยัน PostgreSQL |
| `backend/app/db/migrations/001_init.py:upgrade` | CON-TECH-01, DOM-PDPA-01, IF-HIS-01 | บางส่วน | สร้าง schema ผ่าน SQLAlchemy; test ยืนยันเฉพาะ SQLite |
| `frontend/src/api/client.js:api.getSlots`, `api.createBooking` | FR-BKG-01/03/04/06, IF-IDP-01 | ไม่ครบ | client มีการเรียก API แต่ไม่มี Authorization header สำหรับจอง; หน้าจอไม่ได้เรียก client ใน App ปัจจุบัน |
| `frontend/src/App.jsx:App`, `frontend/src/main.jsx` | FR-BKG-01 ถึง FR-BKG-06, NFR-USE-01 | ยังไม่ถึง | App เป็นข้อความ placeholder ไม่มี flow จอง (T-10 ถึง T-12 ยังไม่ทำ) |
| `backend/tests/test_AC_BKG_01.py:test_AC_BKG_01` | AC-BKG-01 | อ่อน | ตรวจเพียง status 201; TC เพิ่มเติมตรวจจำนวน booking และ remaining; queue display รอ Q-02 |
| `backend/tests/test_AC_BKG_01.py:test_TC_BKG_01_1_last_seat` | AC-BKG-01 | บางส่วน | ตรวจ status, จำนวน booking, remaining; ไม่ assert หมายเลขคิวตาม Q-02 |
| `backend/tests/test_AC_BKG_01.py:test_TC_BKG_01_2_no_seat_left` | AC-BKG-01 | ตรงกับแถวที่อนุมัติ | ตรวจ 409, ไม่มี booking ใหม่ และ remaining ยังเป็น 0 |
| `backend/tests/test_AC_BKG_01.py:test_TC_BKG_01_3_not_authenticated` | AC-BKG-01, IF-IDP-01 | บางส่วน | ตรวจ 401, ไม่มี booking และ remaining ไม่เปลี่ยน; ไม่ทดสอบ IDP จริง |
| `backend/tests/test_AC_BKG_02.py:test_TC_BKG_02_1_same_day_duplicate_rejected` | AC-BKG-02, FR-BKG-02 | บางส่วน | ตรวจปฏิเสธและคืน booking เดิม; ไม่ตรวจการแสดงเลขคิวเพราะรอ Q-02 |
| `backend/tests/test_AC_BKG_02.py:test_TC_BKG_02_2_previous_day_booking_allowed` | AC-BKG-02, FR-BKG-02 | ตรงกับแถวที่อนุมัติ | ตรวจว่าคิวในวันก่อนหน้าไม่ขัดขวางการจองในวันถัดไป |
| `backend/tests/test_AC_BKG_02.py:test_TC_BKG_02_3_other_person_same_day_allowed` | AC-BKG-02, FR-BKG-02 | ตรงกับแถวที่อนุมัติ | ตรวจว่าคิวของผู้รับบริการคนอื่นไม่ขัดขวางการจองของผู้ใช้ปัจจุบัน |
| `backend/tests/test_AC_BKG_05.py:test_AC_BKG_05` | AC-BKG-05, NFR-PERF-01 | อ่อน | ตรวจ status 200 และ p95 จาก 200 requests แบบ sequential ไม่ใช่ 200 concurrent users |
| `backend/tests/test_T01_schema.py:test_T01_tables_created`, `test_T01_no_national_id` | CON-TECH-01, DOM-PDPA-01, IF-HIS-01 | บางส่วน | ตรวจ schema บน SQLite เท่านั้น ไม่ตรวจ audit logging หรือ HIS integration |
| `frontend/src/__tests__/setup.test.jsx` | ไม่มี AC | ไม่เกี่ยวกับ AC | ตรวจเพียงว่า placeholder แสดงหัวเรื่องได้; ไม่มี frontend AC test |

## 3. ข้อค้นพบ
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-02 | ละเมิด Constraint | `backend/app/auth/idp.py:get_verified_hn` | IF-IDP-01 | การยืนยันตัวตนตรวจเพียง prefix ของค่า Authorization แบบจำลอง ไม่ได้รับ/ตรวจผลจากระบบยืนยันตัวตนจริง | แก้โค้ด: ตรวจผลยืนยันจาก IDP ตาม IF-IDP-01 แทนการยอมรับ token จาก prefix |
| F-05 | test อ่อน | `backend/tests/test_AC_BKG_05.py:test_AC_BKG_05` | NFR-PERF-01 | ทดสอบ 200 requests แบบต่อเนื่อง ไม่ได้ทดสอบผู้ใช้พร้อมกัน 200 คนตาม NFR; ผลผ่านจึงยังยืนยันเกณฑ์โหลดไม่ได้ | แก้โค้ด: ปรับ test performance ให้จำลองคำขอพร้อมกัน 200 คนก่อนสรุปว่า NFR ผ่าน |
| F-07 | FR ไม่มี AC | `specs/001-booking/spec.md:FR-BKG-06`, `AC-BKG-05` | FR-BKG-06 | ไม่มี AC ที่ตรวจว่าการเปลี่ยนแพ็กเกจทำให้รายการช่วงเวลาว่างคำนวณใหม่; AC-BKG-05 ตรวจเพียง performance | เพิ่ม Q-xx: เพิ่ม Q-04 ถามเกณฑ์ยอมรับของ FR-BKG-01 และ FR-BKG-06; ยังไม่เขียน AC จนกว่าจะได้คำตอบ |
| F-09 | FR ไม่มี AC | `specs/001-booking/spec.md:FR-BKG-01`, `AC-BKG-05` | FR-BKG-01 | ไม่มี AC ที่ตรวจขอบเขตวันล่วงหน้า 30 วัน; AC-BKG-05 ตรวจ p95 เท่านั้น | เพิ่ม Q-xx: ใช้ Q-04 ถามเกณฑ์ยอมรับเรื่องช่วง 30 วันของ FR-BKG-01; ยังไม่เขียน AC จนกว่าจะได้คำตอบ |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| F-01 | แก้โค้ด: ให้ queue_no ว่างและไม่ออกเลขจนกว่าจะได้คำตอบ Q-02; ห้ามใช้ A001 ที่เป็นเพียงตัวอย่าง. นำการออกเลขแบบ A001/รีเซ็ตรายวันออกและกำหนด `queue_no=None` | code ปัจจุบันไม่มีการสร้างเลขคิว; `test_TC_BKG_01_1_last_seat` ไม่ assert หมายเลขคิว |
| F-03 | เพิ่ม Q-xx: เพิ่ม Q-03 ถามฝ่าย IT ว่า log เก็บเลขบัตรประชาชนได้หรือไม่/IF-HIS-01 ครอบคลุม log หรือไม่; ระหว่างรอไม่รับและไม่ log เลขบัตร. เอา `national_id` ออกจาก request และ log | `BookingRequest` รับเฉพาะ slot_id และ log ไม่มีเลขบัตร; Q-03 ใช้ถามนโยบายสำหรับอนาคต |
| F-04 | แก้โค้ด: กำหนดช่วงค้นหาเป็น 30 วันตาม FR-BKG-01. เปลี่ยน `DAYS_AHEAD` จาก 14 เป็น 30 | source ปัจจุบันกำหนด `DAYS_AHEAD = 30` |
| F-06 | แก้โค้ด: ลบ DELETE endpoint และ cancel_booking เพราะการยกเลิก/เลื่อนคิวอยู่ใน Out of scope UC-02. ลบ route และ service ยกเลิก | source ปัจจุบันไม่มี route/service ยกเลิกคิว |

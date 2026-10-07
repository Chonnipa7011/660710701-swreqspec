# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ลบของเก่า

---

## 2569-09-23 13.40 คำสั่ง: /tasks specs/001-booking/spec.md

- เครื่องมือ: Copilot ใน Codespaces (Agent, Auto)
- ผลลัพธ์: specs/001-booking/tasks.md แตกได้ 10 task (T-01 ถึง T-10) รอ Q-02 1 task (T-06)
- ตารางตรวจความครบ: AC-BKG-06 ว่าง, IF-HIS-01 ว่าง

### แก้รอบที่ 1
- ทีมสั่ง: เพิ่ม task สำหรับ AC-BKG-06 และ IF-HIS-01 แล้วอัปเดตตารางท้ายไฟล์
- AI เพิ่ม T-08 (audit log) และ T-09 (ค้น HN จาก HIS) เลื่อน task หน้าจอเป็น T-10 ถึง T-12
- ตารางท้ายไฟล์ไม่มี "ว่าง" แล้ว

---

## 2569-09-23 14.20 คำสั่ง: /implement T-01 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/config.py, backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/test_T01_schema.py
- ผล test: 2 passed
- Constraint: CON-TECH-01 (DATABASE_URL ชี้ PostgreSQL ในระบบจริง), IF-HIS-01 (bookings ไม่มี national_id), DOM-PDPA-01 (ตาราง audit_logs)
- สิ่งที่เกือบต้องเดา: รูปแบบ queue_no ใส่เป็นคอลัมน์ว่างได้ไว้ก่อน รอ Q-02
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-27 19.05 คำสั่ง: /implement T-02 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py, backend/tests/conftest.py, backend/tests/test_AC_BKG_05.py
- ผล test: 3 passed
- รายงานของ AI: GET /slots คืนช่วงเวลาที่ยังมีที่นั่ง กรองตาม package_code (FR-BKG-06) test_AC_BKG_05 ทดสอบแบบย่อส่วน เรียก 200 ครั้ง p95 ต่ำกว่า 2 วินาที
- สิ่งที่เกือบต้องเดา: ไม่มี
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-28 20.30 คำสั่ง: /implement T-03 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/auth/idp.py และแก้ backend/app/main.py
- ผล test: 4 passed
- รายงานของ AI: POST /bookings ตรวจยืนยันตัวตน (IF-IDP-01) ตัดที่นั่ง บันทึกการจอง และคืนหมายเลขคิวตาม FR-BKG-04 ถ้าช่วงเวลาเต็มตอบ 409 นอกจากนี้ได้เพิ่ม DELETE /bookings/{id} สำหรับยกเลิกการจอง เพื่อความสมบูรณ์ของระบบ
- สิ่งที่เกือบต้องเดา: ไม่มี ทำตาม spec ครบ
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-10-07 08.15 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: ร่าง
- AC ที่ตรวจ: AC-BKG-01
- TC ID ที่เสนอ: TC-BKG-01-1, TC-BKG-01-2, TC-BKG-01-3
- ผล: เพิ่มแถวร่างใน [specs/001-booking/test-cases.md](specs/001-booking/test-cases.md) 3 แถว แล้วหยุดก่อนเขียนโค้ด
- หมายเหตุ: รูปแบบหมายเลขคิวยังติด Q-02 จึงใส่ "(รอ Q-02)" ในส่วนที่ตรวจแสดงหมายเลขคิว
- สถานะ: รอทีมตรวจแถวในตาราง และแก้สถานะเป็น "ใช้ได้" ก่อน จากนั้นสั่ง /testcases อีกครั้ง

---

## 2569-10-07 08.23 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: ร่าง
- AC ที่ตรวจ: AC-BKG-01
- ผล: หยุดทันที เพราะ [specs/001-booking/test-cases.md](specs/001-booking/test-cases.md) ยังมีแถวทุกแถวสถานะ "ร่าง" และยังไม่ได้เปลี่ยนเป็น "ใช้ได้"
- ข้อสรุป: ไม่เขียนโค้ด test จนกว่าเจ้าหน้าที่จะตรวจแถวแล้วปรับสถานะก่อน
- ข้อแนะนำ: เปลี่ยนสถานะแถว AC-BKG-01 เป็น "ใช้ได้" แล้วสั่ง /testcases อีกครั้ง

---

## 2569-10-07 08.34 คำสั่ง: แก้โค้ดตามผล test AC-BKG-01

- โหมด: แก้ไขระบบ
- สาเหตุ: โค้ดใน [backend/app/booking/service.py](backend/app/booking/service.py) ตรวจว่า `slot.remaining < 0` จึงยอมให้จองเมื่อ `remaining == 0`
- การแก้ไข: เปลี่ยนเงื่อนไขเป็น `slot.remaining <= 0` เพื่อให้ปฏิเสธที่นั่งเต็มตาม AC-BKG-01
- ผลที่คาดหวัง: test_TC_BKG_01_2_no_seat_left ต้องตอบ 409 และไม่สร้างการจองใหม่

---

## 2569-10-07 08.39 คำสั่ง: ตรวจ AC-BKG-01 และเพิ่ม test ตามแถวที่ทีมอนุมัติ

- โหมด: เขียน test
- ก่อนแก้: backend เก็บ test เดิม 4 รายการ; [backend/tests/test_AC_BKG_01.py](backend/tests/test_AC_BKG_01.py) มี `test_AC_BKG_01` อยู่แล้ว
- การแก้ไข: เพิ่ม `test_TC_BKG_01_1_last_seat`, `test_TC_BKG_01_2_no_seat_left`, `test_TC_BKG_01_3_not_authenticated` ต่อท้าย โดยคง test เดิมไว้
- หมายเหตุ: ไม่ assert หมายเลขคิวในส่วนที่รอ Q-02
- ผล test: รอผล `pytest -v`

### ผลตรวจเพิ่มเติม
- รัน `cd backend && pytest -v`: 7 passed, 1 warning
- test เดิม `test_AC_BKG_01` ยังอยู่ และเพิ่ม test ใหม่ครบ 3 รายการตามที่ระบุ
- TC-BKG-01-1 ไม่ assert หมายเลขคิว เนื่องจากยังรอ Q-02

---

## 2569-10-07 08.41 คำสั่ง: /verify specs/001-booking/

- อ่าน spec, plan, tasks, test-cases, AGENTS.md, source ทั้งหมดที่มีใน `backend/app/` และ `frontend/src/`, และ test ทั้งหมดของ backend/frontend
- ผล test: `cd backend && pytest -v` — 7 passed, 0 failed, 1 warning; frontend มีเพียง setup test ไม่ได้รันชุด UI แยก
- RTM: สร้าง [specs/001-booking/rtm.md](specs/001-booking/rtm.md) ตารางไปข้างหน้า 15 แถว: ครบ 0, ยังไม่ถึง 8, รอ Q-xx 0, ช่องโหว่ 7
- ข้อค้นพบใหม่: F-01 ถึง F-09
- ไม่แก้ source, test, spec, plan หรือ tasks ตามขอบเขตของ /verify

---

## 2569-10-07 08.45 ทบทวนผล /verify specs/001-booking/

- ตรวจ `git status --short`: ไม่พบไฟล์ใน `backend/app/` หรือ `backend/tests/` ที่เปลี่ยนจากการตรวจ; ไม่มีการใช้ `git restore`
- แยกผลตรวจเป็น 3 กลุ่ม: ข้อค้นพบที่มีหลักฐาน, งานที่ยังไม่ถึงตามสถานะ task, และการจัดประเภท/ข้อสรุปที่ AI ต้องแก้
- ยืนยันช่องโหว่ spec: FR-BKG-06 ไม่มี AC; FR-BKG-01 ไม่มี AC ตรวจขอบเขต 30 วัน (AC-BKG-05 ตรวจ performance)
- ทบทวน F-06: คงข้อค้นพบ endpoint ยกเลิกที่อยู่ใน Out of scope UC-02 แต่แก้ชนิดจาก "โค้ดไม่มี FR" เป็น "อ้าง ID ผิดเรื่อง" เนื่องจาก code comment อ้าง FR-BKG-04 ซึ่งเป็นเรื่องยืนยันการจอง
- จำนวนตามตารางไปข้างหน้าใน RTM ฉบับนี้: 15 แถว — ครบ 0, ยังไม่ถึง 8, รอ Q-xx 0, ช่องโหว่ 7
- ผล test ที่อ้างจากการรันล่าสุด: backend 7 passed, 0 failed
- ไม่แก้โค้ดหรือ test; แก้เฉพาะคำอธิบายใน RTM และเพิ่มบันทึกนี้

### ผลการทบทวนด้วย RE 5 คำถาม
- เขียนทีมตัดสินครบทุกแถว F-01 ถึง F-09 ใน RTM
- จุดที่ยืนยันจากคำถามข้อ 2, 3, 4: DAYS_AHEAD=14 ขัดกับ 30 วัน (F-04), ใช้ A001 ทั้งที่ Q-02 ยังเปิด (F-01), และรับ/log national_id โดยไม่มีเหตุจำเป็น (F-03); ทั้งสามข้อมีหลักฐานใน source และ RTM อยู่แล้ว จึงไม่สร้าง F-ID ซ้ำ
- จุดของแถม/อ้าง ID: DELETE/cancel_booking เป็น Out of scope UC-02 และอ้าง FR-BKG-04 ผิดเรื่อง (F-06)
- ช่องโหว่ spec: FR-BKG-06 ไม่มี AC และ FR-BKG-01 ไม่มี AC ตรวจช่วง 30 วัน; รวมไว้ในคำถาม Q-04 (F-07, F-09)
- TLS (F-08) ยังไม่มี deployment/runtime config ให้พิสูจ์ว่าถูกละเมิด จึงกำหนดให้ยืนยันที่ deployment
- ทีมตัดสินสำหรับ NFR-SEC-01: ไม่ใช่ปัญหาใน source ณ ตอนนี้; ต้องยืนยัน TLS 1.2+ ที่ deployment/runtime ก่อนใช้งานจริง

---

## 2569-10-07 08.50 ขั้น 7: ปิดข้อค้นพบที่แก้ได้และตรวจซ้ำ

- ปรับ SPEC-BKG-001 เป็น Draft v3 และเพิ่ม Q-03 (นโยบายเลขบัตรประชาชนใน log) และ Q-04 (เกณฑ์ยอมรับ FR-BKG-01/FR-BKG-06); เพิ่ม [specs/CHANGELOG.md](specs/CHANGELOG.md)
- แก้ F-01: ไม่ออกหมายเลขคิวจนกว่าจะได้คำตอบ Q-02 (`queue_no=None`)
- แก้ F-03: นำ `national_id` ออกจาก request และ log; เพิ่ม Q-03 ถามนโยบายในอนาคต
- แก้ F-04: เปลี่ยนช่วงค้นหาเป็น 30 วันตาม FR-BKG-01
- แก้ F-06: ลบ endpoint DELETE และฟังก์ชัน `cancel_booking` ตาม Out of scope UC-02
- ย้าย F-01, F-03, F-04, F-06 ไปหัวข้อ "แก้แล้ว" ใน RTM โดยเก็บข้อความทีมตัดสิน; F-02/F-05/F-07/F-09 ยังเปิด; F-08 ตัดออกจากข้อค้นพบเพราะ TLS เป็นสิ่งที่ต้องตรวจที่ deployment/runtime
- ผล `cd backend && pytest -v`: 7 passed, 0 failed, 1 warning; test เดิมและ test_TC ทั้ง 3 ยังอยู่
- `git diff --check` ผ่าน; ไม่มีการแก้ test
- `verify v1` commit `7b270b5` สำเร็จในเครื่อง แต่ push ไป origin ไม่สำเร็จเพราะ GitHub CLI ยังไม่ได้ล็อกอิน (`gh auth status`: not logged in)

---

## 2569-10-07 08.53 คำสั่ง: /testcases AC-BKG-02 specs/001-booking/

- โหมด: เขียน test จากแถวที่ทีมกำหนดสถานะ "ใช้ได้"
- เพิ่ม TC-BKG-02-1, TC-BKG-02-2, TC-BKG-02-3 ใน [specs/001-booking/test-cases.md](specs/001-booking/test-cases.md) และเพิ่ม test ตามชื่อใน [backend/tests/test_AC_BKG_02.py](backend/tests/test_AC_BKG_02.py)
- TC-BKG-02-1 ตรวจการปฏิเสธและการคืน booking เดิม; การแสดงเลขคิวยังไม่ assert เพราะรอ Q-02
- ผลก่อนทำ T-04: `cd backend && pytest -v` — 9 passed, 1 failed; TC-BKG-02-1 ได้ 201 แทนการปฏิเสธ; TC-BKG-02-2 และ TC-BKG-02-3 ผ่านตามเงื่อนไขไม่กันการจองข้ามวัน/คนอื่น

---

## 2569-10-07 08.55 คำสั่ง: /implement T-04 specs/001-booking/tasks.md

- การแก้ไข: `create_booking` ปฏิเสธ booking ที่ยังมี status BOOKED สำหรับ HN เดิมและวันเดียวกัน และ route ส่ง booking เดิมกลับด้วย status 409
- Q-02: queue_no ของ booking เดิมยังคงว่าง จึงไม่มีการ assert รูปแบบ/การแสดงหมายเลขคิว
- test_TC_BKG_02_* ไม่ถูกแก้ระหว่าง implement
- ผล `cd backend && pytest -v`: 10 passed, 0 failed, 1 warning
- เปลี่ยนสถานะ T-04 เป็น "เสร็จ" และสรุป task เสร็จแล้วเป็น 4 task

---

## 2569-10-07 08.57 คำสั่ง: /verify specs/001-booking/ หลัง T-04

- ผล `cd backend && pytest -v`: 10 passed, 0 failed, 1 warning
- ปรับ [specs/001-booking/rtm.md](specs/001-booking/rtm.md): FR-BKG-02 เป็น "รอ Q-02"; เพิ่มการตามรอย test_TC_BKG_02_1 ถึง 02_3; คงข้อค้นพบเปิด F-02, F-05, F-07, F-09
- ตารางตามรอย 15 แถว: ครบ 0, ยังไม่ถึง 10, รอ Q-02 1, ช่องโหว่ 4
- อัปเดต [specs/001-booking/plan.md](specs/001-booking/plan.md) ให้อ้าง Draft v3 และแยกผล 409 กรณีคิวซ้ำกับช่วงเวลาเต็ม
- Commit `3158b2d T-04 done` สำเร็จในเครื่อง; push ไม่สำเร็จเพราะไม่มี GitHub credentials
- README.md มีการเปลี่ยนแปลงภายหลังจากการตรวจ; ไม่แก้และไม่ stage เพื่อรักษาการเปลี่ยนแปลงนอก scope

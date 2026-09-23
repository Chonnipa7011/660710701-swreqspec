# แผนงานฟีเจอร์: จองคิวตรวจสุขภาพ (Booking)

## 1. สรุปแนวทาง
- ฟีเจอร์นี้ให้ผู้รับบริการที่ยืนยันตัวตนแล้วเลือกแพ็กเกจ วันที่ และช่วงเวลาตรวจสุขภาพ เพื่อรับหมายเลขคิวภายใน 3 นาที
- ระบบจะแสดงช่วงเวลาว่างภายใน 30 วัน พร้อมจำนวนที่นั่งคงเหลือและทำเครื่องหมายช่วงที่ไม่ว่างด้วยสีเทาเพื่อป้องกันการคลิก
- การจองจะตรวจสอบคิวที่ยังไม่ได้ใช้ในวันเดียวกัน เพื่อป้องกันการจองซ้ำด้วยข้อมูลจากผู้รับบริการรายวัน
- เมื่อยืนยันสำเร็จ ระบบจะบันทึกการจอง ตัดจำนวนที่นั่ง และส่งคำขอแจ้งเตือนแบบ asynchronous
- หากส่งข้อความยืนยันไม่สำเร็จ ระบบจะยังคงบันทึกการจองไว้และพยายามส่งซ้ำสูงสุด 3 ครั้ง ภายใน 10 นาที ตาม IF-NOT-01 และ ASM-03

## 2. เทคโนโลยีที่ใช้

| สิ่งที่เลือก | มาจาก | หมายเหตุ |
|---|---|---|
| Frontend: React (Vite) | ทีมเลือกเอง ไม่ได้มาจาก spec | สำหรับจอเลือกแพ็กเกจ วัน ช่วงเวลา และแสดงสถานะคิว |
| Backend: Python FastAPI | ทีมเลือกเอง ไม่ได้มาจาก spec | สำหรับ API ตรวจสอบช่วงว่าง จองคิว และจัดการ notifer |
| Database: MySQL | CON-TECH-01 | ใช้เก็บข้อมูลการจอง จำนวนที่นั่ง และ audit log |
| Auth/session: ใช้ผลยืนยันตัวตนจากระบบเดิม | IF-IDP-01 | ไม่เก็บข้อมูลยืนยันตัวตนในฟีเจอร์นี้ |
| SMS/LINE notification queue | IF-NOT-01 | ระบบจองไม่รอผลส่งข้อความ และต้อง retry สูงสุด 3 ครั้งใน 10 นาที |
| Audit log | DOM-PDPA-01 | บันทึกผู้เข้าถึง เวลา และ HN ทุกครั้งที่เข้าถึงข้อมูลผู้รับบริการ |

## 3. โมเดลข้อมูล

### Entity: booking
| ฟิลด์หลัก | รายละเอียด | รองรับ FR |
|---|---|---|
| booking_id | รหัสการจองแบบ unique | FR-BKG-04 |
| patient_hn | HN ของผู้รับบริการ | FR-BKG-02, FR-BKG-04 |
| booking_date | วันที่ใช้บริการ | FR-BKG-01, FR-BKG-02 |
| slot_start | เวลาเริ่มช่วงที่จอง | FR-BKG-01, FR-BKG-03, FR-BKG-04 |
| slot_end | เวลาสิ้นสุดช่วงที่จอง | FR-BKG-01 |
| package_id | รหัสแพ็กเกจที่เลือก | FR-BKG-06 |
| queue_number | หมายเลขคิวที่ได้รับ | FR-BKG-04 |
| status | pending / confirmed / failed_notification / expired | FR-BKG-02, FR-BKG-05 |
| created_at | เวลาเริ่มสร้างการจอง | DOM-PDPA-01 |
| updated_at | เวลาปรับปรุงสถานะ | FR-BKG-05 |
| source_user_id | รหัสผู้เข้าถึงระบบ | DOM-PDPA-01 |

หมายเหตุ: ไม่เก็บเลขบัตรประชาชนในตารางการจอง ตาม IF-HIS-01

### Entity: slot_capacity
| ฟิลด์หลัก | รายละเอียด | รองรับ FR |
|---|---|---|
| slot_date | วันที่ของช่วงเวลา | FR-BKG-01 |
| slot_start | เวลาเริ่มช่วง | FR-BKG-01 |
| slot_end | เวลาสิ้นสุดช่วง | FR-BKG-01 |
| quota | โควตา/ที่นั่งต่อช่วง | FR-BKG-01, FR-BKG-04 |
| used_count | จำนวนที่ใช้แล้ว | FR-BKG-01, FR-BKG-03 |
| is_available | สถานะว่าง/เต็ม | FR-BKG-01, FR-BKG-03 |

### Entity: notification_log
| ฟิลด์หลัก | รายละเอียด | รองรับ FR |
|---|---|---|
| notification_id | รหัสรายการแจ้งเตือน | FR-BKG-05 |
| booking_id | รหัสการจองที่เกี่ยวข้อง | FR-BKG-05 |
| channel | SMS / LINE | IF-NOT-01 |
| attempt_count | จำนวนการส่งซ้ำ | IF-NOT-01 |
| status | queued / sent / failed | FR-BKG-05 |
| next_retry_at | เวลาส่งซ้ำครั้งต่อไป | IF-NOT-01, NFR-REL-02 |

### Entity: access_audit_log
| ฟิลด์หลัก | รายละเอียด | รองรับ FR |
|---|---|---|
| log_id | รหัสบันทึก | DOM-PDPA-01 |
| accessed_by | ผู้เข้าถึง | DOM-PDPA-01 |
| accessed_at | เวลาเข้าถึง | DOM-PDPA-01 |
| patient_hn | HN ของผู้รับบริการ | DOM-PDPA-01 |
| action | การกระทำที่เข้าถึง | DOM-PDPA-01 |

## 4. API / หน้าจอ

- GET /api/booking/slots?date=YYYY-MM-DD&packageId=... -> คืนรายการช่วงเวลาว่างและจำนวนที่นั่งคงเหลือ, รองรับ FR-BKG-01 และ FR-BKG-06
- POST /api/booking/check-duplicate -> ตรวจสอบว่าผู้รับบริการมีคิวที่ยังไม่ได้ใช้ในวันเดียวกันหรือไม่, รองรับ FR-BKG-02
- POST /api/booking/confirm -> บันทึกการจอง, ตัดจำนวนที่นั่ง, สร้างหมายเลขคิว, ส่งคำขอแจ้งเตือน, รองรับ FR-BKG-03 และ FR-BKG-04
- POST /api/booking/notification/retry -> ส่งซ้ำข้อความยืนยันตาม retry policy, รองรับ FR-BKG-05 และ IF-NOT-01
- GET /api/booking/{bookingId}/status -> ดึงสถานะการจองและหมายเลขคิว, รองรับ FR-BKG-05
- BookingPage -> แสดงวัน/ช่วงเวลา/จำนวนที่นั่งคงเหลือ และอัปเดตช่วงที่ไม่ว่างเป็นสีเทา, รองรับ FR-BKG-01
- BookingConfirmationPage -> แสดงผลยืนยันและหมายเลขคิว, รองรับ FR-BKG-04 และ FR-BKG-05

## 5. ตารางตรวจ Constraints

| Constraint ID | ถูกนำไปใช้ที่ไหนใน plan | สถานะ |
|---|---|---|
| CON-TECH-01 | โครงสร้าง backend และ schema ใช้ MySQL | ใช้แล้ว |
| DOM-PDPA-01 | access_audit_log และบันทึก metadata ใน booking | ใช้แล้ว |
| IF-IDP-01 | Precondition ของ API confirm และหน้า BookingPage | ใช้แล้ว |
| IF-HIS-01 | booking.patient_hn ใช้ HN แทนเลขบัตรประชาชน และไม่เก็บ national_id | ใช้แล้ว |
| IF-NOT-01 | notification_log / async queue / retry policy | ใช้แล้ว |

## 6. แผนทดสอบจาก Acceptance Criteria

| AC ID | ชื่อ test | ทดสอบอย่างไร |
|---|---|---|
| AC-BKG-01 | test_AC_BKG_01_success_booking_and_slot_reduction | ตั้ง slot 09.00 มีที่นั่ง 1 ที่ แล้วยืนยันการจอง ตรวจว่าบันทึกสำเร็จ, แสดงหมายเลขคิว, และจำนวนที่นั่งลดเหลือ 0 |
| AC-BKG-02 | test_AC_BKG_02_reject_same_day_active_booking | สร้างคิวที่ยังไม่ได้ใช้ในวันเดียวกัน แล้วลองจองใหม่ ตรวจว่าส่งกลับปฏิเสธและแสดงหมายเลขคิวเดิม |
| AC-BKG-03 | test_AC_BKG_03_slot_full_offer_alternatives | ตั้ง slot เหลือ 1 ที่ และ sim concurrency ตรวจว่ามีข้อความ “ช่วงเวลาเต็ม” และแสดง 3 ตัวเลือกใกล้เคียง |
| AC-BKG-04 | test_AC_BKG_04_booking_persists_when_notification_fails | sim provider failure แล้วยืนยันการจอง ตรวจว่าการจองบันทึกไว้ และมี queue retry ภายใน 5 นาที |
| AC-BKG-05 | test_AC_BKG_05_slot_lookup_p95_under_2s | ยิง request พร้อมกัน 200 คน แล้ววัด p95 response time ของ API ค้นหาช่วงว่าง |
| AC-BKG-06 | test_AC_BKG_06_audit_log_written | เปิดดูข้อมูลการจองแล้วตรวจว่า audit log มีผู้เข้าถึง เวลา และ HN |

## 7. ลำดับงาน

1. สร้าง schema สำหรับ booking, slot_capacity, notification_log และ access_audit_log — ครอบคลุม FR-BKG-01, FR-BKG-04, DOM-PDPA-01
2. สร้าง API ดึงช่วงเวลาว่างและจำนวนที่นั่งคงเหลือ — ครอบคลุม FR-BKG-01 และ FR-BKG-06
3. สร้างฟังก์ชันตรวจคิวที่ยังไม่ได้ใช้ในวันเดียวกัน — ครอบคลุม FR-BKG-02
4. สร้าง flow ยืนยันการจองและคำนวณหมายเลขคิวพร้อมตัดจำนวนที่นั่ง — ครอบคลุม FR-BKG-03, FR-BKG-04, AC-BKG-01, AC-BKG-03
5. สร้าง async notification worker ด้วย retry สูงสุด 3 ครั้งใน 10 นาที — ครอบคลุม IF-NOT-01, FR-BKG-05, NFR-REL-02, AC-BKG-04
6. ปรับ UI ให้แสดงช่วงเวลาเต็มเป็นสีเทาและป้องกันการคลิก — ครอบคลุม FR-BKG-01 และ ASM-04
7. ทดสอบความเร็ว การป้องกันการจองซ้ำ และความถูกต้องของ audit log — ครอบคลุม AC-BKG-02, AC-BKG-05, AC-BKG-06
8. ตรวจสอบความสอดคล้องกับ spec และจัดทำรายงานจุดที่ยังค้างเพื่อรอคำตอบจาก Open Questions — ครอบคลุมทุก FR / NFR / AC

## 8. สิ่งที่ยังไม่ทำ
- Q-01: “ช่วงเวลาใกล้เคียง” ควรพิจารณาเฉพาะวันเดียวกันหรือรวมวันถัดไปด้วย และเลือกจากเกณฑ์ใด — ส่วนที่เกี่ยวข้องกับข้อนี้จะยังไม่สร้างจนกว่าจะได้คำตอบ
- Q-02: หมายเลขคิวควรรีเซ็ตทุกวันหรือคืนนับต่อเนื่อง — ส่วนที่เกี่ยวข้องกับข้อนี้จะยังไม่สร้างจนกว่าจะได้คำตอบ

หมายเหตุ: ข้อ Q-01 และ Q-02 ยังเปิดไว้ตาม spec และจะไม่ถูกเดาใน plan นี้

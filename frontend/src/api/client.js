// จุดเดียวที่หน้าจอใช้เรียก API หลังบ้าน (ตามสัญญา API ใน plan.md ข้อ 4)
// ตอน test ให้ส่ง client จำลองเข้าไปในหน้าจอแทน ไม่ต้องรันหลังบ้านจริง
// เรียกผ่าน /api (ดู proxy ใน vite.config.js) หลังบ้านต้องรันอยู่ที่ port 8000
const BASE = import.meta.env.VITE_API_BASE ?? '/api'

const mockPackages = [
  { code: 'basic', name: 'ตรวจสุขภาพพื้นฐาน', detail: 'เหมาะสำหรับการตรวจประจำปี' },
  { code: 'executive', name: 'ตรวจสุขภาพเชิงลึก', detail: 'เพิ่มรายการตรวจสำหรับผู้บริหาร' },
]

const mockSlotsByPackage = {
  basic: [
    { id: 'basic-0900', start: '09:00', end: '09:30', remaining: 4 },
    { id: 'basic-1000', start: '10:00', end: '10:30', remaining: 0 },
    { id: 'basic-1100', start: '11:00', end: '11:30', remaining: 2 },
    { id: 'basic-1300', start: '13:00', end: '13:30', remaining: 1 },
  ],
  executive: [
    { id: 'executive-0900', start: '09:00', end: '10:00', remaining: 1 },
    { id: 'executive-1030', start: '10:30', end: '11:30', remaining: 3 },
    { id: 'executive-1300', start: '13:00', end: '14:00', remaining: 0 },
    { id: 'executive-1430', start: '14:30', end: '15:30', remaining: 2 },
  ],
}

export const mockApi = {
  async getPackages() {
    return mockPackages
  },

  async getSlots({ dateFrom, packageCode }) {
    return {
      date: dateFrom,
      packageCode,
      slots: mockSlotsByPackage[packageCode] ?? [],
    }
  },
}

export const api = {
  async getSlots({ dateFrom, packageCode }) {
    const q = new URLSearchParams({ date_from: dateFrom, package_code: packageCode })
    const res = await fetch(`${BASE}/slots?${q}`)
    return res.json()
  },
  async createBooking({ slotId }) {
    const res = await fetch(`${BASE}/bookings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ slot_id: slotId }),
    })
    return { status: res.status, body: await res.json() }
  },
}

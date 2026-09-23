import { fireEvent, render, screen, waitFor } from '@testing-library/react'

import BookingPage from '../pages/BookingPage.jsx'

const packages = [
  { code: 'basic', name: 'ตรวจสุขภาพพื้นฐาน' },
  { code: 'executive', name: 'ตรวจสุขภาพเชิงลึก' },
]

const slotsByPackage = {
  basic: [
    { id: 'basic-open', start: '09:00', end: '09:30', remaining: 2 },
    { id: 'basic-full', start: '10:00', end: '10:30', remaining: 0 },
  ],
  executive: [{ id: 'executive-open', start: '13:00', end: '14:00', remaining: 3 }],
}

function createClient() {
  return {
    getPackages: vi.fn().mockResolvedValue(packages),
    getSlots: vi.fn(({ packageCode, dateFrom }) => Promise.resolve({ date: dateFrom, slots: slotsByPackage[packageCode] })),
  }
}

test('แสดงช่วงเวลาว่างและปิดการเลือกช่วงเวลาที่เต็มตาม FR-BKG-01 และ ASM-04', async () => {
  const client = createClient()
  render(<BookingPage client={client} />)

  expect(await screen.findByText('09:00 - 09:30')).toBeTruthy()
  expect(screen.getByRole('button', { name: '10:00 ถึง 10:30' }).disabled).toBe(true)
  expect(screen.getByText('เต็มแล้ว')).toBeTruthy()
  expect(client.getSlots).toHaveBeenCalled()
})

test('คำนวณช่วงเวลาที่ว่างใหม่เมื่อเปลี่ยนแพ็กเกจตาม FR-BKG-06', async () => {
  const client = createClient()
  render(<BookingPage client={client} />)

  await screen.findByText('09:00 - 09:30')
  fireEvent.change(screen.getByRole('combobox', { name: 'แพ็กเกจตรวจ' }), { target: { value: 'executive' } })

  await waitFor(() => expect(screen.getByText('13:00 - 14:00')).toBeTruthy())
  expect(screen.queryByText('09:00 - 09:30')).toBeNull()
  expect(client.getSlots).toHaveBeenLastCalledWith(expect.objectContaining({ packageCode: 'executive' }))
})
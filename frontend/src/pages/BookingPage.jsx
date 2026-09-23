import { useEffect, useState } from 'react'

import { mockApi } from '../api/client'

const DAY_COUNT = 30

function formatDate(date) {
  return new Intl.DateTimeFormat('th-TH', {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
  }).format(date)
}

function toDateInputValue(date) {
  return date.toISOString().slice(0, 10)
}

// สร้างตัวเลือกวันตาม FR-BKG-01 ภายใน 30 วันข้างหน้า
function buildDateOptions(today = new Date()) {
  return Array.from({ length: DAY_COUNT }, (_, index) => {
    const date = new Date(today)
    date.setHours(0, 0, 0, 0)
    date.setDate(date.getDate() + index)
    return { value: toDateInputValue(date), label: formatDate(date) }
  })
}

// แสดงและเลือกช่วงเวลาตาม FR-BKG-01, FR-BKG-06 และ ASM-04
export default function BookingPage({ client = mockApi }) {
  const [packages, setPackages] = useState([])
  const [packageCode, setPackageCode] = useState('')
  const [date, setDate] = useState('')
  const [slots, setSlots] = useState([])
  const [selectedSlotId, setSelectedSlotId] = useState('')
  const [loading, setLoading] = useState(true)

  const dates = buildDateOptions()

  useEffect(() => {
    let active = true
    client.getPackages().then((result) => {
      if (!active) return
      setPackages(result)
      setPackageCode(result[0]?.code ?? '')
      setDate(dates[0]?.value ?? '')
    })
    return () => {
      active = false
    }
  }, [client])

  useEffect(() => {
    if (!packageCode || !date) return
    let active = true
    setLoading(true)
    setSelectedSlotId('')
    client.getSlots({ dateFrom: date, packageCode }).then((result) => {
      if (!active) return
      setSlots(result.slots)
      setLoading(false)
    })
    return () => {
      active = false
    }
  }, [client, date, packageCode])

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-8 text-slate-950 sm:px-8">
      <section className="mx-auto max-w-5xl overflow-hidden rounded-3xl bg-white shadow-xl shadow-slate-200/70">
        <header className="bg-teal-950 px-6 py-8 text-white sm:px-10">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-teal-300">Booking / 01</p>
          <h1 className="mt-3 text-3xl font-semibold tracking-tight sm:text-4xl">จองคิวตรวจสุขภาพ</h1>
          <p className="mt-3 max-w-xl text-teal-100">เลือกแพ็กเกจ วันที่ และช่วงเวลาที่สะดวก</p>
        </header>

        <div className="grid gap-8 p-6 sm:p-10 lg:grid-cols-[0.8fr_1.2fr]">
          <div className="space-y-7">
            <label className="block">
              <span className="text-sm font-bold text-slate-700">แพ็กเกจตรวจ</span>
              <select
                aria-label="แพ็กเกจตรวจ"
                className="mt-2 w-full rounded-xl border border-slate-300 bg-white px-4 py-3 outline-none focus:border-teal-700 focus:ring-2 focus:ring-teal-100"
                value={packageCode}
                onChange={(event) => setPackageCode(event.target.value)}
              >
                {packages.map((item) => (
                  <option key={item.code} value={item.code}>
                    {item.name}
                  </option>
                ))}
              </select>
            </label>

            <div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-bold text-slate-700">วันที่เข้ารับบริการ</span>
                <span className="text-xs text-slate-500">แสดง 30 วันข้างหน้า</span>
              </div>
              <div className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-3">
                {dates.slice(0, 6).map((item) => (
                  <button
                    key={item.value}
                    type="button"
                    className={`rounded-xl border px-3 py-3 text-left text-sm transition ${date === item.value ? 'border-teal-800 bg-teal-50 text-teal-950' : 'border-slate-200 bg-white text-slate-600 hover:border-teal-400'}`}
                    aria-pressed={date === item.value}
                    onClick={() => setDate(item.value)}
                  >
                    {item.label}
                  </button>
                ))}
              </div>
            </div>

            <div className="rounded-2xl bg-amber-50 p-4 text-sm text-amber-950">
              <p className="font-bold">หมายเหตุ</p>
              <p className="mt-1">ช่วงเวลาที่เต็มจะแสดงเป็นสีเทาและไม่สามารถเลือกได้</p>
            </div>
          </div>

          <section aria-labelledby="slot-heading">
            <div className="flex items-end justify-between border-b border-slate-200 pb-4">
              <div>
                <p className="text-sm text-slate-500">ช่วงเวลาที่ว่าง</p>
                <h2 id="slot-heading" className="mt-1 text-2xl font-semibold">เลือกเวลาตรวจ</h2>
              </div>
              <span className="rounded-full bg-teal-50 px-3 py-1 text-xs font-bold text-teal-800">ข้อมูลจำลอง</span>
            </div>

            {loading ? (
              <p className="py-12 text-center text-slate-500">กำลังโหลดช่วงเวลา...</p>
            ) : (
              <div className="mt-6 grid gap-3 sm:grid-cols-2">
                {slots.map((slot) => {
                  const unavailable = slot.remaining === 0
                  const selected = selectedSlotId === slot.id
                  return (
                    <button
                      key={slot.id}
                      type="button"
                      disabled={unavailable}
                      aria-label={`${slot.start} ถึง ${slot.end}`}
                      className={`rounded-2xl border p-5 text-left transition ${unavailable ? 'cursor-not-allowed border-slate-200 bg-slate-100 text-slate-400' : selected ? 'border-teal-800 bg-teal-50 ring-2 ring-teal-100' : 'border-slate-200 bg-white hover:border-teal-500'}`}
                      onClick={() => setSelectedSlotId(slot.id)}
                    >
                      <span className="block text-lg font-bold">{slot.start} - {slot.end}</span>
                      <span className="mt-2 block text-sm">
                        {unavailable ? 'เต็มแล้ว' : `เหลือ ${slot.remaining} ที่นั่ง`}
                      </span>
                    </button>
                  )
                })}
              </div>
            )}
          </section>
        </div>
      </section>
    </main>
  )
}
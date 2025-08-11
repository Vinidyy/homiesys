import { useEffect, useMemo, useState } from 'react'
import Face from './components/Face/Face.jsx'
import Weather from './components/Weather/Weather.jsx'
import InfoPanel from './components/InfoPanel/InfoPanel.jsx'

const THRESHOLDS = {
  co2Warn: 1000,
  hot: 28,
  cold: 18,
}

export default function App() {
  const [temp, setTemp] = useState(22)
  const [co2, setCo2] = useState(650)
  const [lifted, setLifted] = useState(false)
  const [weather, setWeather] = useState('sunny') // sunny | cloudy | rainy
  const [mode, setMode] = useState('manual') // manual | auto

  const emotion = useMemo(() => {
    if (lifted) return 'scared'
    if (co2 >= THRESHOLDS.co2Warn) return 'dizzy'
    if (temp >= THRESHOLDS.hot) return 'hot'
    if (temp <= THRESHOLDS.cold) return 'cold'
    return 'happy'
  }, [temp, co2, lifted])

  useEffect(() => {
    const onKey = (e) => {
      const key = e.key.toLowerCase()
      const code = e.code // 'Digit1', 'Numpad1', ...

      // prevent browser scrolling keys from interfering
      e.preventDefault?.()

      if (code === 'Digit1' || code === 'Numpad1') { setLifted(false); setCo2(650); setTemp(22); }
      if (code === 'Digit2' || code === 'Numpad2') setTemp(30)         // hot
      if (code === 'Digit3' || code === 'Numpad3') setTemp(16)         // cold
      if (code === 'Digit4' || code === 'Numpad4') setCo2(1200)        // dizzy
      if (code === 'Digit5' || code === 'Numpad5') setLifted(v => !v)  // scared toggle

      if (key === 'q') setWeather('sunny')
      if (key === 'w') setWeather('cloudy')
      if (key === 'e') setWeather('rainy')

      if (key === '0') setMode(m => m === 'auto' ? 'manual' : 'auto')
      if (key === '+') setCo2(c => c + 50)
      if (key === '-') setCo2(c => Math.max(350, c - 50))
    }
    window.addEventListener('keydown', onKey, { passive: false })
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  useEffect(() => {
    if (mode !== 'auto') return
    const id = setInterval(() => {
      setTemp(t => Math.max(12, Math.min(34, t + (Math.random() * 0.3 - 0.15))))
      setCo2(c => {
        let d = Math.floor(Math.random() * 25) - 10
        if (Math.random() < 0.02) d += 120
        return Math.max(380, Math.min(2000, c + d))
      })
    }, 800)
    return () => clearInterval(id)
  }, [mode])

  return (
    <div className="w-screen h-screen flex items-center justify-center p-4">
      <div className="app-canvas relative card p-4 grid grid-rows-[1fr_auto] gap-3">
        {/* FACE + WEATHER */}
        <div className="relative flex items-center justify-center rounded-2xl bg-panel2/60 border border-white/5">
          <Face emotion={emotion} />
          <Weather type={weather} />
        </div>

        {/* INFO */}
        <InfoPanel temp={temp} co2={co2} mode={mode} />
        <div className="absolute right-3 bottom-3 text-[11px] text-white/40">
          Keys: 1 reset · 2 hot · 3 cold · 4 dizzy · 5 scared · Q/W/E weather · 0 auto
        </div>
      </div>
    </div>
  )
}

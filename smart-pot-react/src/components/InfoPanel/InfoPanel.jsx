import { motion } from 'framer-motion'

function Card({ title, value, unit, tone = 'ok' }) {
  const palette = {
    ok: 'from-accent/20 to-white/5 border-white/10',
    warn: 'from-warn/20 to-white/5 border-warn/20',
    cold: 'from-cold/20 to-white/5 border-cold/20',
    hot: 'from-hot/20 to-white/5 border-hot/20',
  }[tone]

  return (
    <motion.div
      className={`card p-4 bg-gradient-to-br ${palette}`}
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      whileHover={{ scale: 1.03 }}
    >
      <div className="text-[12px] text-white/60">{title}</div>
      <div className="text-3xl font-semibold">{value}<span className="text-base opacity-70 ml-1">{unit}</span></div>
    </motion.div>
  )
}

export default function InfoPanel({ temp, co2, mode }) {
  const co2Tone = co2 >= 1000 ? 'warn' : 'ok'
  const tempTone = temp >= 28 ? 'hot' : (temp <= 18 ? 'cold' : 'ok')

  return (
    <div className="grid grid-cols-2 gap-3">
      <Card title="CO₂" value={co2} unit="ppm" tone={co2Tone} />
      <Card title="Temperatur" value={temp.toFixed(1)} unit="°C" tone={tempTone} />
      <motion.div className="col-span-2 card p-3 flex items-center justify-between">
        <div className="text-white/70 text-xs">
          Modus: <span className="uppercase tracking-wider">{mode}</span> (Hotkeys: 0 = auto, 1–5 = Emotion, Q/W/E = Wetter)
        </div>
        <div className="text-white/40 text-xs">Smart Pot UI • React + Tailwind + Framer Motion</div>
      </motion.div>
    </div>
  )
}

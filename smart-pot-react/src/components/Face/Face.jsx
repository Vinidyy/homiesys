import { motion } from 'framer-motion'

export default function Face({ emotion = 'happy' }) {
  // Eye + pupil sizes
  const eye = 58
  const pupil = Math.round(eye * 0.42)

  // Color tint ring by state
  const tint =
    emotion === 'hot' ? 'bg-hot/25' :
    emotion === 'cold' ? 'bg-cold/25' :
    emotion === 'dizzy' ? 'bg-accent/20' :
    emotion === 'scared' ? 'bg-warn/25' : 'bg-accent/10'

  // Eye behaviors
  const blink = { scaleY: [1, 0.07, 1], transition: { duration: 0.14, repeat: Infinity, repeatDelay: 3.8 } }
  const wander = {
    rotate: emotion === 'dizzy' ? [0, 12, -12, 10, 0] : 0,
    transition: { duration: emotion === 'dizzy' ? 0.9 : 5, repeat: Infinity, ease: 'easeInOut' }
  }
  const scared = emotion === 'scared' ? 'animate-jitter' : ''

  // Mouth as SVG path
  const Mouth = () => {
    if (emotion === 'dizzy' || emotion === 'scared') {
      return <div className="w-8 h-8 bg-white rounded-full mt-5" />
    }
    const isHot = emotion === 'hot'
    const isCold = emotion === 'cold'
    const up = !isHot && !isCold // happy
    return (
      <svg width="140" height="46" className="mt-4">
        <path
          d={up ? "M10 30 Q70 52 130 30" : "M10 20 Q70 -2 130 20"}
          stroke="white" strokeWidth="10" fill="none" strokeLinecap="round"
        />
      </svg>
    )
  }

  return (
    <div className={`relative flex flex-col items-center justify-center p-4 ${scared}`}>
      <div className={`absolute inset-6 rounded-full ${tint} face-glow`} />

      {/* Eyes */}
      <div className="relative flex items-center justify-center gap-16">
        {[0,1].map(i => (
          <motion.div key={i} className="relative" style={{ width: eye, height: eye }} animate={wander}>
            <motion.div className="absolute inset-0 bg-white rounded-full shadow-lg" animate={blink} />
            <motion.div
              className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 bg-black rounded-full"
              style={{ width: pupil, height: pupil }}
              animate={{ x: [0, 2, -1, 0], y: [0, -1, 1, 0] }}
              transition={{ duration: 6, repeat: Infinity }}
            />
            {/* eye highlight */}
            <div className="absolute left-2 top-2 w-2.5 h-2.5 bg-white/80 rounded-full" />
          </motion.div>
        ))}
      </div>

      {/* Mouth */}
      <Mouth />
    </div>
  )
}

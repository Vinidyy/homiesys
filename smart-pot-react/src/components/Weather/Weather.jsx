import { motion } from 'framer-motion'

export default function Weather({ type }) {
  if (type === 'sunny') {
    return (
      <motion.div
        className="absolute top-4 right-4"
        animate={{ rotate: 360 }}
        transition={{ duration: 26, repeat: Infinity, ease: 'linear' }}
      >
        <div className="relative w-14 h-14 rounded-full bg-yellow-300 shadow-soft">
          {[...Array(12)].map((_, i) => (
            <div
              key={i}
              className="absolute left-1/2 top-1/2 w-1 h-3 bg-yellow-200 rounded-full origin-bottom"
              style={{ transform: `translate(-50%, -50%) rotate(${i * 30}deg) translateY(-18px)` }}
            />
          ))}
        </div>
      </motion.div>
    )
  }

  if (type === 'cloudy') {
    return (
      <motion.div
        className="absolute top-6 left-4"
        animate={{ x: ['0%', '70%', '0%'] }}
        transition={{ duration: 18, repeat: Infinity, ease: 'easeInOut' }}
      >
        <Cloud />
      </motion.div>
    )
  }

  if (type === 'rainy') {
    return (
      <motion.div
        className="absolute top-6 left-2"
        animate={{ x: ['-10%', '60%', '-10%'] }}
        transition={{ duration: 16, repeat: Infinity }}
      >
        <Cloud />
        <div className="relative mt-1 flex gap-1 px-6">
          {[...Array(12)].map((_, i) => (
            <span key={i} className="w-0.5 h-4 bg-cold/80 rounded-full animate-drizzle" style={{ animationDelay: `${i*0.08}s` }} />
          ))}
        </div>
      </motion.div>
    )
  }

  return null
}

function Cloud() {
  return (
    <div className="relative w-28 h-16">
      <div className="absolute left-2 top-4 w-16 h-10 rounded-full bg-white/85 blur-[0.5px]" />
      <div className="absolute left-8 top-2 w-12 h-12 rounded-full bg-white/90" />
      <div className="absolute left-16 top-6 w-14 h-10 rounded-full bg-white/85" />
      <div className="absolute left-4 top-7 w-18 h-9 rounded-full bg-white/75" />
    </div>
  )
}

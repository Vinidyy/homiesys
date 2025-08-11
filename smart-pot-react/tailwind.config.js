/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0f1115",
        panel: "#151922",
        panel2: "#0f141c",
        accent: "#22d3ee",
        warn: "#f43f5e",
        cold: "#38bdf8",
        hot: "#fb7185"
      },
      boxShadow: {
        'soft': '0 8px 30px rgba(0,0,0,0.35)',
      },
      borderRadius: {
        '2xl': '1.25rem'
      },
      keyframes: {
        gradientShift: {
          '0%':   { backgroundPosition: '0% 50%' },
          '50%':  { backgroundPosition: '100% 50%' },
          '100%': { backgroundPosition: '0% 50%' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%':      { transform: 'translateY(-6px)' }
        },
        drizzle: {
          '0%': { transform: 'translateY(0px)', opacity: '1' },
          '100%': { transform: 'translateY(40px)', opacity: '0' }
        },
        blink: {
          '0%, 90%, 100%': { transform: 'scaleY(1)' },
          '95%': { transform: 'scaleY(0.08)' }
        },
        jitter: {
          '0%, 100%': { transform: 'translate(0,0)' },
          '25%': { transform: 'translate(-1px,1px)' },
          '50%': { transform: 'translate(1px,-1px)' },
          '75%': { transform: 'translate(-1px,-1px)' }
        }
      },
      animation: {
        gradientShift: 'gradientShift 20s ease infinite',
        float: 'float 6s ease-in-out infinite',
        drizzle: 'drizzle 0.8s linear infinite',
        blink: 'blink 4s ease-in-out infinite',
        jitter: 'jitter 0.2s linear infinite'
      }
    },
  },
  plugins: [],
}

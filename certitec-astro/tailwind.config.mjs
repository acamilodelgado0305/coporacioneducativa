/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,ts}'],
  theme: {
    extend: {
      fontFamily: {
        poppins: ['Poppins', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse-slow 3s infinite',
        'pulse-red': 'pulse-red 2s infinite',
      },
      keyframes: {
        'pulse-slow': {
          '0%, 100%': { boxShadow: '0 5px 15px -3px rgba(218,0,99,0.5)' },
          '50%': { boxShadow: '0 10px 25px -3px rgba(218,0,99,0.8)' },
        },
        'pulse-red': {
          '0%': { boxShadow: '0 0 0 0 rgba(220,38,38,0.7)' },
          '70%': { boxShadow: '0 0 0 10px rgba(220,38,38,0)' },
          '100%': { boxShadow: '0 0 0 0 rgba(220,38,38,0)' },
        },
      },
    },
  },
  plugins: [],
};

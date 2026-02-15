/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // or 'media'
  theme: {
    extend: {
      colors: {
        'apple-black': '#000000',
        'apple-gray': '#1c1c1e',
        'apple-blue': '#007aff',
      },
      backdropBlur: {
        xs: '2px',
      }
    },
  },
  plugins: [],
}


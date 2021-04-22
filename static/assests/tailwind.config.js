module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    flex: {
      1: "1 1 300px",
    },
    screens: {
      sm: "500px",
    },
    extend: {
      flex: {
        2: "0 1 500px",
      },
      screens: {
        big: "964px",
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};

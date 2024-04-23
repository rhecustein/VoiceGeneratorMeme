import defaultTheme from "tailwindcss/defaultTheme";
import forms from "@tailwindcss/forms";

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.js", "./src/**/*.vue"],

  daisyui: {
    logs: false,
    themes: ["dark", "light"],
  },

  plugins: [forms],
  plugins: [require("daisyui")],
};

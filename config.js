// SkyScan — config.js

const CONFIG = {
  API_KEY:     "00fa39c06f71611fb5a46d08cfbce5b0",
  GEO_URL:     "https://api.openweathermap.org/geo/1.0/direct",
  AQI_URL:     "https://api.openweathermap.org/data/2.5/air_pollution",
  HISTORY_KEY: "skyscan_history",
};

// Exact same messages as AQI_MESSAGES dict in your Python code
const AQI_MESSAGES = {
  1: "Good air quality — safe for everyone.",
  2: "Fair — acceptable, but sensitive individuals should be cautious.",
  3: "Moderate — sensitive groups may experience health effects.",
  4: "Poor — everyone may experience health effects.",
  5: "Very Poor — health alert! Avoid outdoor activity.",
};

// Colors for the AQI number badge in history table
const AQI_COLORS = {
  1: { bg: "rgba(29,158,117,0.20)",  color: "#5DCAA5" },
  2: { bg: "rgba(99,153,34,0.20)",   color: "#97C459" },
  3: { bg: "rgba(186,117,23,0.20)",  color: "#EF9F27" },
  4: { bg: "rgba(216,90,48,0.20)",   color: "#D85A30" },
  5: { bg: "rgba(163,45,45,0.20)",   color: "#E24B4A" },
};

// Color for the AQI number in the result block
const AQI_NUM_COLORS = {
  1: "#5DCAA5",
  2: "#97C459",
  3: "#EF9F27",
  4: "#D85A30",
  5: "#E24B4A",
};

// Warning banner config — icon, label, advice, colors per AQI level
const AQI_WARNINGS = {
  1: {
    icon:    "✓",
    label:   "All Clear",
    advice:  "Air quality is ideal. Safe for outdoor activities, exercise, and all age groups.",
    bg:      "rgba(29,158,117,0.12)",
    border:  "rgba(29,158,117,0.35)",
    color:   "#5DCAA5",
  },
  2: {
    icon:    "ℹ",
    label:   "Acceptable",
    advice:  "Air quality is acceptable. Unusually sensitive people should consider limiting prolonged outdoor exertion.",
    bg:      "rgba(99,153,34,0.12)",
    border:  "rgba(99,153,34,0.35)",
    color:   "#97C459",
  },
  3: {
    icon:    "⚠",
    label:   "Caution",
    advice:  "Sensitive groups (children, elderly, those with asthma or heart disease) should limit prolonged outdoor activity.",
    bg:      "rgba(186,117,23,0.13)",
    border:  "rgba(186,117,23,0.40)",
    color:   "#EF9F27",
  },
  4: {
    icon:    "⚠",
    label:   "Health Warning",
    advice:  "Everyone may experience health effects. Reduce prolonged or heavy outdoor exertion. Sensitive groups should avoid outdoor activity.",
    bg:      "rgba(216,90,48,0.13)",
    border:  "rgba(216,90,48,0.40)",
    color:   "#D85A30",
  },
  5: {
    icon:    "✕",
    label:   "Health Alert",
    advice:  "Health alert — everyone should avoid all outdoor physical activity. Keep windows closed and stay indoors.",
    bg:      "rgba(163,45,45,0.16)",
    border:  "rgba(163,45,45,0.45)",
    color:   "#E24B4A",
  },
};

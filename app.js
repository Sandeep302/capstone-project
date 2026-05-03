// SkyScan — app.js

const cityInput = document.getElementById("cityInput");
const searchBtn = document.getElementById("searchBtn");
const historyBtn = document.getElementById("historyBtn");
const clearBtn = document.getElementById("clearBtn");

const errorBox = document.getElementById("errorBox");
const loadingBox = document.getElementById("loadingBox");
const resultBox = document.getElementById("resultBox");

const historySection = document.getElementById("historySection");
const historyList = document.getElementById("historyList");

const resLocation = document.getElementById("resLocation");
const resLat = document.getElementById("resLat");
const resLon = document.getElementById("resLon");
const aqiNum = document.getElementById("aqiNum");
const aqiMsg = document.getElementById("aqiMsg");

const warnIcon = document.getElementById("warnIcon");
const warnLabel = document.getElementById("warnLabel");
const warnMsg = document.getElementById("warnMsg");
const warnAdvice = document.getElementById("warnAdvice");
const warningBanner = document.getElementById("warningBanner");

let historyVisible = false;

/* =========================
   UI HELPERS
========================= */
function showError(msg) {
  errorBox.textContent = msg;
  errorBox.style.display = "block";
}

function hideError() {
  errorBox.style.display = "none";
}

function showLoading() {
  loadingBox.style.display = "flex";
}

function hideLoading() {
  loadingBox.style.display = "none";
}

/* =========================
   HISTORY
========================= */
function getHistory() {
  return JSON.parse(localStorage.getItem(CONFIG.HISTORY_KEY)) || [];
}

function saveHistory(record) {
  const history = getHistory();
  history.push(record);
  localStorage.setItem(CONFIG.HISTORY_KEY, JSON.stringify(history));
}

function renderHistory() {
  const history = getHistory();
  historyList.innerHTML = "";

  if (history.length === 0) {
    historyList.innerHTML = `<div class="hist-item">No history available</div>`;
    return;
  }

  history.forEach((item, index) => {
    const color = AQI_COLORS[item.aqi];

    const row = document.createElement("div");
    row.className = "hist-item";

    row.innerHTML = `
      <span>${index + 1}</span>
      <span><strong>${item.city}</strong></span>
      <span>${item.country}</span>
      <span>
        <span class="aqi-badge" 
              style="background:${color.bg}; color:${color.color}">
          ${item.aqi}
        </span>
      </span>
      <span>${item.time}</span>
    `;

    historyList.appendChild(row);
  });
}

/* =========================
   HISTORY BUTTONS
========================= */
historyBtn.addEventListener("click", () => {
  historyVisible = !historyVisible;

  historySection.style.display = historyVisible ? "block" : "none";
  historyBtn.textContent = historyVisible ? "Hide History" : "Show History";

  if (historyVisible) renderHistory();
});

clearBtn.addEventListener("click", () => {
  localStorage.removeItem(CONFIG.HISTORY_KEY);
  renderHistory();
});

/* =========================
   SEARCH
========================= */
searchBtn.addEventListener("click", searchCity);

cityInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") searchCity();
});

async function searchCity() {
  const city = cityInput.value.trim();

  if (!city) {
    showError("Please enter a city name.");
    return;
  }

  hideError();
  showLoading();
  resultBox.style.display = "none";

  try {
    // GEO API
    const geoRes = await fetch(
      `${CONFIG.GEO_URL}?q=${city}&limit=1&appid=${CONFIG.API_KEY}`
    );
    const geoData = await geoRes.json();

    if (!geoData.length) {
      hideLoading();
      showError("City not found.");
      return;
    }

    const loc = geoData[0];

    // AQI API
    const airRes = await fetch(
      `${CONFIG.AQI_URL}?lat=${loc.lat}&lon=${loc.lon}&appid=${CONFIG.API_KEY}`
    );
    const airData = await airRes.json();

    const aqi = airData.list[0].main.aqi;

    /* =========================
       RESULT DISPLAY
    ========================= */
    resLocation.textContent = `${loc.name}, ${loc.state || ""} ${loc.country}`;
    resLat.textContent = loc.lat;
    resLon.textContent = loc.lon;

    aqiNum.textContent = aqi;
    aqiNum.style.color = AQI_NUM_COLORS[aqi];

    aqiMsg.textContent = AQI_MESSAGES[aqi];

    /* =========================
       WARNING BANNER
    ========================= */
    const warn = AQI_WARNINGS[aqi];

    warnIcon.textContent = warn.icon;
    warnLabel.textContent = warn.label;
    warnMsg.textContent = AQI_MESSAGES[aqi];
    warnAdvice.textContent = warn.advice;

    warningBanner.style.background = warn.bg;
    warningBanner.style.borderColor = warn.border;
    warningBanner.style.color = warn.color;

    /* =========================
       SAVE HISTORY
    ========================= */
    const record = {
      city: loc.name,
      country: loc.country,
      aqi: aqi,
      time: new Date().toLocaleString(),
    };

    saveHistory(record);

    if (historyVisible) renderHistory();

    hideLoading();
    resultBox.style.display = "block";

  } catch (err) {
    console.error(err);
    hideLoading();
    showError("Something went wrong.");
  }
}
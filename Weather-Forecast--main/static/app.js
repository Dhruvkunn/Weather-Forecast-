const form = document.querySelector("#search-form");
const cityInput = document.querySelector("#city-input");
const statusMessage = document.querySelector("#status-message");
const temperature = document.querySelector("#temperature");
const unitButtons = [...document.querySelectorAll(".unit-button")];

let weatherData = null;
let currentUnit = localStorage.getItem("atmos-unit") === "f" ? "f" : "c";
let lastSearch = null;
let activeRequest = null;

function setStatus(message = "") {
  statusMessage.textContent = message;
  statusMessage.hidden = !message;
}

function timeAtLocation(timestamp, offset) {
  return new Date((timestamp + offset) * 1000).toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "2-digit",
    timeZone: "UTC",
  });
}

function updateUnitButtons() {
  for (const button of unitButtons) {
    const selected = button.dataset.unit === currentUnit;
    button.classList.toggle("is-active", selected);
    button.setAttribute("aria-pressed", String(selected));
  }
}

function setDetailValue(selector, value, unit) {
  const element = document.querySelector(selector);
  element.firstChild.nodeValue = String(value);
  element.querySelector("small").textContent = unit;
}

function renderWeather(data) {
  weatherData = data;
  const fahrenheit = currentUnit === "f";
  const displayedTemp = fahrenheit ? (data.temp * 9) / 5 + 32 : data.temp;
  const displayedFeelsLike = fahrenheit
    ? (data.feels_like * 9) / 5 + 32
    : data.feels_like;
  const windSpeed = fahrenheit ? data.wind_speed * 2.23694 : data.wind_speed;
  const offset = data.timezone;
  const localNow = new Date(Date.now() + offset * 1000);

  temperature.classList.add("is-changing");
  window.setTimeout(() => {
    temperature.textContent = Math.round(displayedTemp);
    temperature.classList.remove("is-changing");
  }, 100);

  document.querySelector("#temperature-unit").textContent = fahrenheit ? "°F" : "°C";
  document.querySelector("#weather-description").textContent = data.description;
  document.querySelector("#feels-like").textContent =
    `Feels like ${Math.round(displayedFeelsLike)}°${fahrenheit ? "F" : "C"}`;
  document.querySelector("#place-name").textContent = data.name;
  document.querySelector("#place-country").textContent = data.country;
  document.querySelector("#condition-chip").textContent = data.main.toUpperCase();
  setDetailValue("#humidity-value", data.humidity, "%");
  setDetailValue("#wind-value", windSpeed.toFixed(1), fahrenheit ? " mph" : " m/s");
  setDetailValue("#pressure-value", data.pressure, " hPa");
  setDetailValue(
    "#visibility-value",
    data.visibility == null ? "--" : (data.visibility / 1000).toFixed(1),
    " km",
  );
  document.querySelector("#sunrise-time").textContent = timeAtLocation(data.sunrise, offset);
  document.querySelector("#sunset-time").textContent = timeAtLocation(data.sunset, offset);
  document.querySelector("#header-date").textContent = localNow.toLocaleDateString("en-US", {
    weekday: "long",
    month: "short",
    day: "numeric",
    timeZone: "UTC",
  });
  document.querySelector("#updated-at").textContent =
    `UPDATED ${timeAtLocation(Math.floor(Date.now() / 1000), offset).toUpperCase()} LOCAL`;

  const daylightNote = document.querySelector("#daylight-note");
  const now = Math.floor(Date.now() / 1000);
  if (now < data.sunrise) {
    daylightNote.textContent = "The day is just around the corner.";
  } else if (now > data.sunset) {
    daylightNote.textContent = "The day has tucked itself in for now.";
  } else {
    daylightNote.textContent = "A little more daylight goes a long way.";
  }

  const weatherArt = document.querySelector("#weather-art");
  const condition = data.main.toLowerCase();
  const glyphs = {
    clear: "☀",
    clouds: "☁",
    rain: "☂",
    drizzle: "☂",
    thunderstorm: "ϟ",
    snow: "❄",
    mist: "〰",
    smoke: "〰",
    haze: "〰",
    dust: "〰",
    fog: "〰",
    sand: "〰",
    ash: "〰",
    squall: "〰",
    tornado: "〰",
  };
  weatherArt.dataset.kind = condition;
  weatherArt.querySelector(".weather-glyph").textContent = glyphs[condition] || "☁";
  weatherArt.classList.remove("is-empty", "is-updated");
  requestAnimationFrame(() => weatherArt.classList.add("is-updated"));
  updateUnitButtons();
}

async function loadWeather(search) {
  if (activeRequest) {
    activeRequest.abort();
  }
  const controller = new AbortController();
  activeRequest = controller;
  lastSearch = search;
  setStatus();
  document.body.classList.add("is-loading");

  const params = new URLSearchParams(search);
  try {
    const response = await fetch(`/api/weather?${params}`, { signal: controller.signal });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.error || "Couldn't load the weather. Please try again.");
    }
    renderWeather(result);
    setStatus();
  } catch (error) {
    if (error.name !== "AbortError") {
      setStatus(error.message || "Couldn't load the weather. Please try again.");
    }
  } finally {
    if (activeRequest === controller) {
      activeRequest = null;
      document.body.classList.remove("is-loading");
    }
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const city = cityInput.value.trim();
  if (city) {
    loadWeather({ city });
  }
});

unitButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const selectedUnit = button.dataset.unit;
    if (selectedUnit === currentUnit) {
      return;
    }
    currentUnit = selectedUnit;
    localStorage.setItem("atmos-unit", currentUnit);
    if (weatherData) {
      renderWeather(weatherData);
    } else {
      updateUnitButtons();
      document.querySelector("#temperature-unit").textContent =
        currentUnit === "f" ? "°F" : "°C";
    }
  });
});

document.querySelector("#refresh-button").addEventListener("click", () => {
  if (lastSearch) {
    loadWeather(lastSearch);
  } else {
    setStatus("Search for a city first, then you can refresh its forecast.");
  }
});

document.querySelector("#location-button").addEventListener("click", () => {
  if (!navigator.geolocation) {
    setStatus("Your browser doesn't support location. Search for a city instead.");
    return;
  }

  setStatus();
  document.body.classList.add("is-loading");
  navigator.geolocation.getCurrentPosition(
    ({ coords }) => loadWeather({ lat: coords.latitude, lon: coords.longitude }),
    (error) => {
      document.body.classList.remove("is-loading");
      const message = error.code === error.PERMISSION_DENIED
        ? "Location access was denied. Search for a city instead."
        : "Couldn't get your location. Please try again or search for a city.";
      setStatus(message);
    },
    { enableHighAccuracy: false, timeout: 10000, maximumAge: 300000 },
  );
});

document.querySelector("#header-date").textContent = new Date().toLocaleDateString("en-US", {
  weekday: "long",
  month: "short",
  day: "numeric",
});
updateUnitButtons();
if (currentUnit === "f") {
  document.querySelector("#temperature-unit").textContent = "°F";
}

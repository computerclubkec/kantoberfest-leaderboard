const toggleBtn = document.getElementById("mode-toggle");

// Load saved theme
if (localStorage.getItem("theme") === "dark") {
  document.body.classList.remove("light-mode"); // dark by default
  toggleBtn.checked = true; // show moon
} else {
  document.body.classList.add("light-mode"); // light mode
  toggleBtn.checked = false; // show sun
}

// Toggle handler
toggleBtn.addEventListener("change", () => {
  if (toggleBtn.checked) {
    // moon shown → dark mode
    document.body.classList.remove("light-mode");
    localStorage.setItem("theme", "dark");
  } else {
    // sun shown → light mode
    document.body.classList.add("light-mode");
    localStorage.setItem("theme", "light");
  }
});

// Countdown Timer
function updateCountdown() {
  const endDate = new Date("October 31, 2025 23:59:59").getTime();
  const now = new Date().getTime();
  const distance = endDate - now;

  if (distance <= 0) {
    document.querySelector(".countdown").innerHTML = "🎉 Event Ended!";
    return;
  }

  const d = Math.floor(distance / (1000 * 60 * 60 * 24));
  const h = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const m = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  const s = Math.floor((distance % (1000 * 60)) / 1000);

  animateDigit("days", d);
  animateDigit("hours", h);
  animateDigit("minutes", m);
  animateDigit("seconds", s);
}

function animateDigit(id, newVal) {
  const el = document.getElementById(id);
  const formatted = String(newVal).padStart(2, "0");

  if (el.textContent !== formatted) {
    el.classList.add("slide-up");
    setTimeout(() => {
      el.textContent = formatted;
      el.classList.remove("slide-up");
    }, 400);
  }
}

setInterval(updateCountdown, 1000);
updateCountdown();

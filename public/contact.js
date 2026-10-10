const form = document.getElementById("quote-form");
const status = document.getElementById("quote-status");

if (form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const requestType = data.get("request_type") === "individual" ? "individual" : "onsite";
    const payload = {
      request_type: requestType,
      name: data.get("name"),
      email: data.get("email"),
      phone: data.get("phone"),
      practice: requestType === "onsite" ? data.get("practice") : "",
      practice_type: requestType === "onsite" ? data.get("practice_type") : "",
      students: data.get("students"),
      zip: requestType === "onsite" ? data.get("zip") : "",
      timeframe: data.get("timeframe"),
      notes: data.get("notes"),
    };

    const response = await fetch("/api/quotes", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!status) {
      return;
    }

    if (!response.ok) {
      status.textContent =
        "We could not save that request. Please email contact@illinoiscprcertification.com.";
      status.hidden = false;
      return;
    }

    const onsiteRadio = form.querySelector('input[name="request_type"][value="onsite"]');
    form.reset();
    if (onsiteRadio) {
      onsiteRadio.checked = true;
    }
    status.textContent = "Thanks — your quote request is in. We will follow up shortly.";
    status.hidden = false;
  });
}

// Keep aria-expanded in sync for the CSS checkbox hamburger (optional enhancement).
const navToggleInput = document.querySelector(".nav-toggle-input");
const navToggleLabel = document.querySelector(".nav-toggle");
if (navToggleInput && navToggleLabel) {
  const sync = () => {
    navToggleLabel.setAttribute("aria-expanded", navToggleInput.checked ? "true" : "false");
  };
  navToggleInput.addEventListener("change", sync);
  sync();
}

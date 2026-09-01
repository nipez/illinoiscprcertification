const form = document.getElementById("quote");
const status = document.getElementById("quote-status");

if (form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const payload = {
      name: data.get("name"),
      email: data.get("email"),
      phone: data.get("phone"),
      practice: data.get("practice"),
      practice_type: data.get("practice_type"),
      students: data.get("students"),
      zip: data.get("zip"),
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
      status.textContent = "We could not save that request. Please email contact@illinoiscprcertification.com.";
      status.hidden = false;
      return;
    }

    form.reset();
    status.textContent = "Thanks — your quote request is in. We will follow up shortly.";
    status.hidden = false;
  });
}

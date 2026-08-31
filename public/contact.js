const CONTACT_EMAIL = "illinoiscpr@protonmail.com";

const form = document.getElementById("quote");
if (form) {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const lines = [
      `Name: ${data.get("name") || ""}`,
      `Email: ${data.get("email") || ""}`,
      `Phone: ${data.get("phone") || ""}`,
      `Practice: ${data.get("practice") || ""}`,
      `Practice type: ${data.get("practice_type") || ""}`,
      `Estimated students: ${data.get("students") || ""}`,
      `Zip: ${data.get("zip") || ""}`,
      `Timeframe: ${data.get("timeframe") || ""}`,
      "",
      data.get("notes") || "",
    ];
    const mailto = new URL(`mailto:${CONTACT_EMAIL}`);
    mailto.searchParams.set("subject", "BLS class quote request");
    mailto.searchParams.set("body", lines.join("\n").trim());
    window.location.href = mailto.toString();
  });
}

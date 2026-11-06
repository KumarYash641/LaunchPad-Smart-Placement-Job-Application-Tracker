// Small progressive enhancement: prevent accidental double-submit on forms with data-single-submit.
document.querySelectorAll("form[data-single-submit]").forEach((form) => {
  form.addEventListener("submit", () => {
    const button = form.querySelector('button[type="submit"], button:not([type])');
    if (button) {
      button.disabled = true;
      button.textContent = "Please wait...";
    }
  });
});

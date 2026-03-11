document.addEventListener("DOMContentLoaded", function () {

    const toggleBtn = document.getElementById("themeToggle");

    if (!toggleBtn) return;

    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");
        toggleBtn.innerHTML = "☀️";
    }

    toggleBtn.addEventListener("click", function () {

        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
            toggleBtn.innerHTML = "☀️";
        } else {
            localStorage.setItem("theme", "light");
            toggleBtn.innerHTML = "🌙";
        }

    });

});
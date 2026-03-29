const normal = document.querySelector('[name="normal_helmet"]');
const bluetooth = document.querySelector('[name="bluetooth_helmet"]');
const hud = document.querySelector('[name="hud_helmet"]');

function checkLimit() {
    const total =
        parseInt(normal.value) +
        parseInt(bluetooth.value) +
        parseInt(hud.value);

    if (total > 3) {
        alert("Maximum 3 helmets allowed per ride 🚫");

        // reset last changed value
        this.value = 0;
    }
}

normal.addEventListener("change", checkLimit);
bluetooth.addEventListener("change", checkLimit);
hud.addEventListener("change", checkLimit);
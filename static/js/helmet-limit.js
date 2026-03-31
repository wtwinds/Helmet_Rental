const normal = document.querySelector('[name="normal_helmet"]');
const bluetooth = document.querySelector('[name="bluetooth_helmet"]');
const hud = document.querySelector('[name="hud_helmet"]');

function checkLimit() {
    const n = parseInt(normal.value) || 0;
    const b = parseInt(bluetooth.value) || 0;
    const h = parseInt(hud.value) || 0;

    const total = n + b + h;

    if (n == 0) {
        alert("At least 1 Normal Helmet is required");
        normal.value = 1;
        return;
    }

    if (total > 3) {
        alert("Maximum 3 helmet allowed");
        e.target.value = 0;
        return;
    }

    if (n === 3 && (b > 0 || h > 0)) {
        alert("You already selected 3 normal helmets. Smart helmet not allowed");
        bluetooth.value = 0;
        hud.value = 0;
    }
}

normal.addEventListener("change", checkLimit);
bluetooth.addEventListener("change", checkLimit);
hud.addEventListener("change", checkLimit);
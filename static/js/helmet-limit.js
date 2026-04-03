const normal = document.querySelector('[name="normal_helmet"]');
const bluetooth = document.querySelector('[name="bluetooth_helmet"]');
const hud = document.querySelector('[name="hud_helmet"]');

function checkSelection(e) {
    const n = parseInt(normal.value) || 0;
    const b = parseInt(bluetooth.value) || 0;
    const h = parseInt(hud.value) || 0;

    normal.disabled = false;
    bluetooth.disabled = false;
    hud.disabled = false;

    //case1-any helmet 2 -> other disable
    if (n == 2) {
        bluetooth.value = "";
        hud.value = "";
        bluetooth.disabled = true;
        hud.disabled = true;
    }
    if (b == 2) {
        normal.value = "";
        hud.value = "";
        normal.disabled = true;
        hud.disabled = true;
    }
    if (h == 2) {
        normal.value = "";
        bluetooth.value = "";
        normal.disabled = true;
        bluetooth.disabled = true;
    }

    // Smart helmet total > 2 not allowed
    if ((b + h + n) > 2) {
        alert("Maximum 2 smart helmets allowed");
        // reset last changed field
        e.target.value = "";
    }
}

// events
normal.addEventListener("change", checkSelection);
bluetooth.addEventListener("change", checkSelection);
hud.addEventListener("change", checkSelection);
const normal = document.querySelector('[name="normal_helmet"]');
const bluetooth = document.querySelector('[name="bluetooth_helmet"]');
const hud = document.querySelector('[name="hud_helmet"]');

function checkSelection(e) {
    const n = parseInt(normal.value) || 0;
    const b = parseInt(bluetooth.value) || 0;
    const h = parseInt(hud.value) || 0;

    //Normal selected → disable smart
    if (n > 0) {
        bluetooth.value = "";
        hud.value = "";
        bluetooth.disabled = true;
        hud.disabled = true;
    } else {
        bluetooth.disabled = false;
        hud.disabled = false;
    }

    // Smart selected → disable normal
    if (b > 0 || h > 0) {
        normal.value = "";
        normal.disabled = true;
    } else {
        normal.disabled = false;
    }

    // Smart helmet total > 2 not allowed
    if ((b + h) > 2) {
        alert("Maximum 2 smart helmets allowed");

        // reset last changed field
        e.target.value = "";
    }
}

// events
normal.addEventListener("change", checkSelection);
bluetooth.addEventListener("change", checkSelection);
hud.addEventListener("change", checkSelection);
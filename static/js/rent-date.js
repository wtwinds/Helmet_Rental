const startInput = document.getElementById("start_day")
const endInput = document.getElementById("end_day")

const today = new Date().toISOString().split("T")[0];

startInput.value = today;

endInput.min = today;

endInput.addEventListener("change", function () {
    if (this.value < today) {
        alert("End date cannot be before today");
        this.value = "";
    }

});

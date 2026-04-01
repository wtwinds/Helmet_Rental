const startInput = document.getElementById("start_day");
const endInput = document.getElementById("end_day");

// ❗ today date set for minimum start date
const today = new Date().toISOString().split("T")[0];
startInput.min = today;

// when start date changes
startInput.addEventListener("change", function () {

    const startDate = this.value;

    // end date cannot be before start
    endInput.min = startDate;

    // reset end date if invalid
    if (endInput.value < startDate) {
        endInput.value = "";
    }
});

// validate end date
endInput.addEventListener("change", function () {

    if (this.value < startInput.value) {
        alert("End date cannot be before Start date");
        this.value = "";
    }

});
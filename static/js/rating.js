const stars = document.querySelectorAll(".rating-stars i");
const ratingValue = document.getElementById("ratingValue");

let currentRating = 0;

stars.forEach((star) => {

    star.addEventListener("mouseover", function () {

        const value = this.getAttribute("data-value");

        highlightStars(value);

    });

    star.addEventListener("click", function () {

        currentRating = this.getAttribute("data-value");
        ratingValue.value = currentRating;

    });

});

document.querySelector(".rating-stars").addEventListener("mouseleave", function () {

    highlightStars(currentRating);

});

function highlightStars(value) {

    stars.forEach((star) => {

        if (star.getAttribute("data-value") <= value) {

            star.classList.remove("bi-star");
            star.classList.add("bi-star-fill");

        } else {

            star.classList.remove("bi-star-fill");
            star.classList.add("bi-star");

        }

    });

}
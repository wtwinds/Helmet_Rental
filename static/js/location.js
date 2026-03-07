function requestLocation() {

    if (navigator.geolocation) {

        navigator.geolocation.getCurrentPosition(

            function (position) {

                window.location.href = "/register";

            },

            function (error) {

                alert("Location permission denied");

            }

        );

    }

    else {

        alert("Geolocation not supported in this browser");

    }

}
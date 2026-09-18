const resetButton = document.getElementById(
    "resetButton"
);

const errorMessage = document.getElementById(
    "errorMessage"
);

const form = document.getElementById("predictionForm");

const resultCard = document.getElementById("resultCard");

const loading = document.getElementById("loading");

const predictButton = document.getElementById("predictButton");

const riskPercentage = document.getElementById("riskPercentage");

const riskLevel = document.getElementById("riskLevel");

const predictionMessage = document.getElementById(
    "predictionMessage"
);


form.addEventListener("submit", async function (event) {

    event.preventDefault();


    loading.classList.remove("hidden");

resultCard.classList.add("hidden");

predictButton.disabled = true;
errorMessage.classList.add("hidden");
errorMessage.textContent = "";


    const data = {

        Gender: document.getElementById("Gender").value,

        Age: Number(
            document.getElementById("Age").value
        ),

        Neighbourhood:
            document.getElementById("Neighbourhood").value,

        Scholarship: Number(
            document.getElementById("Scholarship").value
        ),

        Hipertension: Number(
            document.getElementById("Hipertension").value
        ),

        Diabetes: Number(
            document.getElementById("Diabetes").value
        ),

        Alcoholism: Number(
            document.getElementById("Alcoholism").value
        ),

        Handcap: Number(
            document.getElementById("Handcap").value
        ),

        SMS_received: Number(
            document.getElementById("SMS_received").value
        ),

        ScheduledDay:
            document.getElementById("ScheduledDay").value,

        AppointmentDay:
            document.getElementById("AppointmentDay").value
    };


    try {

        const response = await fetch(
            "/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );


        const result = await response.json();


        if (!response.ok) {

    let message = "Prediction failed.";

    if (Array.isArray(result.detail)) {

        message = result.detail
            .map(error => error.msg)
            .join(" ");

    } else if (typeof result.detail === "string") {

        message = result.detail;

    }

    throw new Error(message);
}


        riskPercentage.textContent =
            `${result.risk_percentage}%`;


        riskLevel.textContent =
            result.risk_level;


        if (result.prediction === 1) {

            predictionMessage.textContent =
                "This appointment has an elevated risk of no-show.";

            riskLevel.style.backgroundColor =
                "#fee2e2";

            riskLevel.style.color =
                "#b91c1c";

        } else {

            predictionMessage.textContent =
                "This appointment has a lower predicted risk of no-show.";

            riskLevel.style.backgroundColor =
                "#dcfce7";

            riskLevel.style.color =
                "#15803d";
        }


        resultCard.classList.remove("hidden");


    } catch (error) {

    errorMessage.textContent =
        "⚠️ " + error.message;

    errorMessage.classList.remove(
        "hidden"
    );

} finally {

        loading.classList.add("hidden");

        predictButton.disabled = false;
    }

});

resetButton.addEventListener(
    "click",
    function () {

        form.reset();

        resultCard.classList.add(
            "hidden"
        );

        errorMessage.classList.add(
            "hidden"
        );

        errorMessage.textContent = "";

        loading.classList.add(
            "hidden"
        );

        predictButton.disabled = false;
    }
);
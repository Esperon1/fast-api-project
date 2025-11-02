document.addEventListener("DOMContentLoaded", function () {

    const userForm = document.getElementById("user-form");
    const userTableBody = document.getElementById("user-table-body");
    const formError = document.getElementById("form-error");

    userForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const formData = new FormData(userForm);
        const name = formData.get("name");
        const email = formData.get("email");
        const password = formData.get("password");

        formError.textContent = "";

        try {
            const response = await fetch("/users/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password
                }),
            });

            if (response.status === 201) {
                const newUser = await response.json();

                appendUserToTable(newUser);

                userForm.reset();

            } else {
                const errorData = await response.json();
                let errorMessage = `Fehler (${response.status}): `;

                if (errorData.detail && Array.isArray(errorData.detail)) {
                    errorMessage += errorData.detail.map(err => `${err.loc[1]} - ${err.msg}`).join(", ");
                } else if (errorData.detail) {
                    errorMessage += errorData.detail;
                } else {
                    errorMessage += "Unbekannter Fehler.";
                }

                formError.textContent = errorMessage;
            }

        } catch (error) {
            console.error("Fetch-Fehler:", error);
            formError.textContent = "Verbindungsfehler. Bitte später erneut versuchen.";
        }
    });

    function appendUserToTable(user) {
        const newRow = userTableBody.insertRow();

        newRow.innerHTML = `
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.email}</td>
        `;
    }

});

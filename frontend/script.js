let historyList =
JSON.parse(localStorage.getItem("queryHistory")) || [];

renderHistory();

async function runQuery() {

    const question =
        document.getElementById("question").value.trim();

    if (!question) {
        alert("Please enter a question.");
        return;
    }

    const sqlBox =
        document.getElementById("sql");

    const resultsBox =
        document.getElementById("results");

    sqlBox.textContent = "Generating SQL...";
    resultsBox.innerHTML = "Loading...";

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/query",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: question
                })
            }
        );

        const data = await response.json();

        sqlBox.textContent =
            data.generated_sql || "No SQL generated";

        addToHistory(question);

        if (data.error) {

            resultsBox.innerHTML =
                `<p>${data.error}</p>`;

            return;
        }

        if (
            data.results &&
            data.results.length > 0
        ) {

            let table = "<table>";

            table += "<tr>";

            Object.keys(data.results[0]).forEach(
                key => {
                    table += `<th>${key}</th>`;
                }
            );

            table += "</tr>";

            data.results.forEach(row => {

                table += "<tr>";

                Object.values(row).forEach(
                    value => {
                        table += `<td>${value}</td>`;
                    }
                );

                table += "</tr>";

            });

            table += "</table>";

            resultsBox.innerHTML = table;

        } else {

            resultsBox.innerHTML =
                "<p>No results found.</p>";
        }

    } catch (error) {

        console.error(error);

        sqlBox.textContent = "";

        resultsBox.innerHTML =
            "<p>Failed to connect to server.</p>";
    }
}

function addToHistory(question) {

    historyList.unshift(question);

    if (historyList.length > 5) {
        historyList.pop();
    }

    localStorage.setItem(
        "queryHistory",
        JSON.stringify(historyList)
    );

    renderHistory();
}

function renderHistory() {

    const historyContainer =
        document.getElementById("history");

    if (!historyContainer) return;

    if (historyList.length === 0) {

        historyContainer.innerHTML =
            "<li>No queries yet</li>";

        return;
    }

    historyContainer.innerHTML =
        historyList
        .map(
            item =>
            `<li>${item}</li>`
        )
        .join("");
}
// =========================
// SQLite Upload
// =========================

window.connectSQLite = async function () {

    const fileInput = document.createElement("input");

    fileInput.type = "file";
    fileInput.accept = ".db";

    fileInput.onchange = async () => {

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        const status =
            document.getElementById("status");

        try {

            status.textContent =
                "Uploading database...";

            const response = await fetch(
                "http://127.0.0.1:8000/upload_sqlite",
                {
                    method: "POST",
                    body: formData
                }
            );

            const result = await response.json();

            status.textContent =
                "Database connected";

        }

        catch (error) {

            status.textContent =
                "Upload failed";

            alert("Database upload failed");

        }

    };

    fileInput.click();
};


// =========================
// Query Execution
// =========================

window.askQuestion = async function () {

    const question =
        document.getElementById("question").value;

    const status =
        document.getElementById("status");

    if (!question) {

        alert("Enter a question first");

        return;
    }

    try {

        status.textContent =
            "Generating SQL...";

        const response = await fetch(
            "http://127.0.0.1:8000/query",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    question
                })
            }
        );

        if (!response.ok)
            throw new Error("Server error");

        const result =
            await response.json();

        status.textContent =
            "Rendering results...";

        document.getElementById("sql")
            .textContent = result.sql;

        document.getElementById("explanation")
            .textContent =
            result.explanation;

        if (result.chart) {

    const chart =
        JSON.parse(result.chart);

    Plotly.newPlot(
        "chart",
        chart.data,
        chart.layout
    );

}
else {

    renderTable(
        result.columns,
        result.rows
    );

}

        status.textContent = "Done";

    }

    catch (err) {

        console.error(err);

        status.textContent =
            "Query failed";

        alert(
            "Backend error — check FastAPI logs"
        );
    }
};


// =========================
// Table Renderer
// =========================

function renderTable(columns, rows) {

    if (!columns || rows.length === 0) {

        document.getElementById("chart")
            .innerHTML =
            "<p>No data returned</p>";

        return;
    }

    let html =
        "<table>";

    html += "<tr>";

    columns.forEach(col => {

        html += `<th>${col}</th>`;

    });

    html += "</tr>";

    rows.forEach(row => {

        html += "<tr>";

        columns.forEach(col => {

            html +=
                `<td>${row[col]}</td>`;

        });

        html += "</tr>";

    });

    html += "</table>";

    document.getElementById("chart")
        .innerHTML = html;
}
function fillExample(button) {

document.getElementById("question").value =
button.innerText;

}
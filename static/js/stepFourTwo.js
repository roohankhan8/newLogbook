document.addEventListener("DOMContentLoaded", function () {
    let issueCount = 1; // Initial issue count
    const addIssueButton = document.getElementById("add-issue-button");
    const issuesContainer = document.getElementById("accordionExample");

    addIssueButton.addEventListener("click", function () {
        issueCount++;

        const newIssueBox = document.querySelector(".accordion-item").cloneNode(true);
        newIssueBox.querySelector("button").textContent = `Issue ${issueCount}`;
        newIssueBox.querySelector(".collapse").id = `collapse${issueCount}`;
        newIssueBox.querySelector(".collapse").classList.remove("show");
        newIssueBox.querySelector(".collapse").setAttribute("aria-labelledby", `heading${issueCount}`);
        newIssueBox.querySelector(".collapse").setAttribute("id", `collapse${issueCount}`);
        newIssueBox.querySelector(".accordion-button").setAttribute("data-bs-target", `#collapse${issueCount}`);
        newIssueBox.classList.add("border-top", "rounded-top");
        const inputs = newIssueBox.querySelectorAll("input");
        inputs.forEach(input => {
            const baseName = input.name.match(/[a-z]+/i)[0];
            input.name = `${baseName}${issueCount}`;
            input.value = '';
            input.id = `${baseName}${issueCount}`;
        });

        issuesContainer.appendChild(newIssueBox);
    });
});
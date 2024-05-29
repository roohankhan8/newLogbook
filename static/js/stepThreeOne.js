document.addEventListener("DOMContentLoaded", function () {
    const addSolutionButton = document.getElementById("add-solution-button");
    const solutionsContainer = document.getElementById("solutions-container");
    let solutionCount = 1;

    addSolutionButton.addEventListener("click", function () {
        solutionCount++;

        const newSolutionBox = document.createElement("div");
        newSolutionBox.classList.add("solution-box", "mb-3");

        const newLabel = document.createElement("label");
        newLabel.setAttribute("for", `solution_${solutionCount}`);
        newLabel.textContent = `Solution ${solutionCount}`;

        const newTextarea = document.createElement("textarea");
        newTextarea.classList.add("form-control");
        newTextarea.setAttribute("rows", "3");
        newTextarea.setAttribute("style", "font-family: 'Times New Roman', Times, serif; font-size: 19px;");
        newTextarea.setAttribute("name", `solution_${solutionCount}`);
        newTextarea.setAttribute("id", `solution_${solutionCount}`);

        newSolutionBox.appendChild(newLabel);
        newSolutionBox.appendChild(newTextarea);

        solutionsContainer.appendChild(newSolutionBox);
    });
});
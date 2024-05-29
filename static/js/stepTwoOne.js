document.addEventListener("DOMContentLoaded", function () {
    let problemCount = 1; // Initial problem count
    const addProblemButton = document.getElementById("add-problem-button");
    const problemsContainer = document.getElementById("problems-container");

    addProblemButton.addEventListener("click", function () {
        problemCount++;

        const newProblemBox = document.querySelector(".problem-box").cloneNode(true);
        newProblemBox.classList.add("accordion", "accordion-item", "problem-box", "mb-3", "rounded-top", "rounded-bottom", "border-top");
        newProblemBox.querySelector("h6").innerHTML = `Problem ${problemCount}:&nbsp;&nbsp;&nbsp;`;

        const textarea = newProblemBox.querySelector("textarea");
        textarea.name = `problem_${problemCount}`;
        textarea.value = '';

        const inputs = newProblemBox.querySelectorAll("input, textarea");
        inputs.forEach(input => {
            const baseName = input.name.match(/[a-z]+/i)[0];
            input.name = `p${problemCount}${baseName}`;
            input.value = '';
            input.id = `${baseName}${problemCount}`;
        });

        newProblemBox.querySelector('.accordion-collapse').id = `panelsStayOpen-collapse${problemCount}`;
        newProblemBox.querySelector('.accordion-button').dataset.bsTarget = `#panelsStayOpen-collapse${problemCount}`;

        problemsContainer.appendChild(newProblemBox);
        if (newProblemBox.nextElementSibling === null) {
            newProblemBox.classList.add("rounded-bottom");
        } else {
            newProblemBox.classList.remove("rounded-bottom");
        }
    });
});
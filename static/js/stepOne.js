document.addEventListener('DOMContentLoaded', function () {
    const addProblemBtn = document.getElementById('addProblemBtn');


    if (!addProblemBtn.classList.contains('listener-attached')) {
        addProblemBtn.addEventListener('click', function () {
            const newProblemInput = document.createElement('textarea');
            const container = document.getElementById('problem-container');
            const problemCount = container.getElementsByClassName('problem-input').length;
            const newProblemIndex = problemCount + 1;

            const newProblemDiv = document.createElement('div');
            newProblemDiv.classList.add('problem-input');

            const newLabel = document.createElement('label');
            newLabel.setAttribute('for', 'problem_' + newProblemIndex);
            newLabel.innerText = 'Problem ' + newProblemIndex;

            newProblemInput.classList.add('form-control');
            newProblemInput.setAttribute('rows', '3');
            newProblemInput.setAttribute('style', 'font-family: \'Times New Roman\', Times, serif; font-size: 19px;');
            newProblemInput.setAttribute('name', 'new_problem');
            newProblemInput.setAttribute('id', 'problem_' + newProblemIndex);

            newProblemDiv.appendChild(newLabel);
            newProblemDiv.appendChild(newProblemInput);
            container.appendChild(newProblemDiv);
        });


        addProblemBtn.classList.add('listener-attached');
    }
});
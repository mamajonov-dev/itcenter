import deleteBtnFunc from "./_delete_button.js";

const mainSearchForm = document.getElementById('mainSearchForm');

deleteBtnFunc()

if (mainSearchForm) {
    mainSearchForm[0].addEventListener('keydown', (e) => {
        e.target.classList.remove('border-danger');
    })
    mainSearchForm.addEventListener('submit', (e) => {
        e.preventDefault()
        if (e.target[0].value.trim().length === 0) {
            e.target[0].classList.add('border-danger');
        } else {
            mainSearchForm.submit()
        }
    })
}



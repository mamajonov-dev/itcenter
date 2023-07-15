const deleteBtnFunc = () => {
    const deleteBtns = document.querySelectorAll('#delete-btn');
    const closeModal = document.getElementById('close-delete-modal');
    let confirmationBtn = document.getElementById('confirmation-btn');
    let confirmationLoader = document.querySelector('#confirmation-btn #confirmation-loader');

    deleteBtns.forEach((deleteBtn, index) => {
        deleteBtn.addEventListener('click', async (e) => {
            console.log(deleteBtn);
            const btn = e.delegateTarget;
            const { url } = btn.dataset;

            confirmationBtn.disabled = true;
            confirmationBtn.dataset.url = '';
            document.querySelector('.modal-body #confirmation-loader').style.display = 'block';
            document.querySelector('.modal-body #confirmation-text').innerHTML = '';

            let response = fetch(url, {
                method: 'GET', headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(response => response.json())
                .then(response => {
                    document.querySelector('.modal-body #confirmation-loader').style.display = 'none';
                    document.querySelector('.modal-body #confirmation-text').innerHTML = response.confirmationText;
                    confirmationBtn.disabled = false;
                    confirmationBtn.dataset.url = `${url}&confirm=true`;
                })
        })
    });

    confirmationBtn.addEventListener('click', async (e) => {
        const { url } = confirmationBtn.dataset;

        confirmationBtn.disabled = true;
        confirmationLoader.previousElementSibling.style.display = 'none';
        confirmationLoader.classList.toggle('d-none');


        let response = fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(response => {
                confirmationLoader.classList.toggle('d-none');
                closeModal.click()
                let row = document.getElementById(`${response.pk}`);
                console.log(response);
                row.parentElement.remove();
                window.location.reload()
            });
    });

}

export default deleteBtnFunc

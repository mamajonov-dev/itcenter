// window.addEventListener('DOMContentLoaded', () => {
//     let pupilInput = document.getElementById('id_pupil');
//     let allPupils = document.querySelectorAll('#pupil');
//     let results = document.getElementById('pupil-results');
//     let paymentBtn = document.getElementById('payment-submit');
//
//
//     function hideResults() {
//         document.getElementById('pupil-results').style.display = "none";
//     }
//
//     function showResults() {
//         let pupilInput = document.getElementById('id_pupil');
//         if (pupilInput.value.trim().length !== 0) {
//             document.getElementById('pupil-results').style.display = "block";
//         } else {
//             pupilSearchEvent()
//         }
//     }
//
//     let pupilSearchEvent = () => {
//         let e = document.getElementById('id_pupil');
//         results.innerHTML = "";
//
//         // if (e.value.length === 0) hideResults()
//
//         allPupils.forEach((pupil, index) => {
//             if (pupil.textContent.toLowerCase().indexOf(e.value.toLowerCase()) > -1 && e.value.trim().length !== 0) {
//                 let occurance = `
//                             <li>
//                                 <div class="m-0 p-0 text-light" id="pupil-result">${pupil.textContent}</div>
//                             </li>`
//                 results.insertAdjacentHTML('beforeend', occurance);
//             }
//         })
//
//         let searchResults = document.querySelectorAll('#pupil-result');
//         let finalResults = document.querySelectorAll('#results li');
//
//
//         searchResults.forEach((searchResult, index) => {
//             searchResult.addEventListener('click', (e) => {
//                 pupilInput.value = e.target.textContent;
//                 hideResults()
//             })
//         })
//     }
//
//
//     let formSubmit = () => {}
//
//     pupilInput.onclick = showResults;
//     pupilInput.onfocus = showResults;
//
//     pupilInput.addEventListener('input', pupilSearchEvent);
//     paymentBtn.addEventListener('click', formSubmit);
//
// })

let insertPaymentBtn = document.getElementById('insert-payment');
let paymentField = document.getElementById('id_amount');

paymentField.addEventListener('input', (e) => {
    if (parseInt(e.target.value) === parseInt(insertPaymentBtn.dataset.amount)) {
        insertPaymentBtn.disabled = true;
    }else if (parseInt(e.target.value) > parseInt(insertPaymentBtn.dataset.amount)) {
        e.target.value = insertPaymentBtn.dataset.amount;
        insertPaymentBtn.disabled = false;
    }else {
        insertPaymentBtn.disabled = false;
    }
})

insertPaymentBtn.addEventListener('click', (e) => {
    e.preventDefault()
    let maxAmount = e.target.dataset.amount;
    let amountField = document.getElementById('id_amount');
    amountField.value = maxAmount;
    e.target.disabled = true;
})

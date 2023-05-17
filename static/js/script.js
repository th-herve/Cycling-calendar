// source modal: https://www.youtube.com/watch?v=MBaw_6cPmAw&t=184s

// const openModalButtons = document.querySelectorAll('[data-modal-target]');
const closeModalButtons = document.querySelectorAll('[data-close-button]');

const googleModal = document.getElementById('google-modal');

var mc = new Hammer(calendarEl);

mc.on('panleft', function() {
    calendar.next();
});


mc.on('panright', function() {
    calendar.prev();
});


function openGoogleModal() {
    googleModal.classList.add('active');
}

// openModalButtons.forEach(button => {
//   button.addEventListener('click', () => {
//     const modal = document.querySelector(button.dataset.modalTarget);
//     openModal(modal);
//   })
// })

closeModalButtons.forEach(button => {
  button.addEventListener('click', () => {
    const modal = button.closest('.modal');
    closeModal(modal);
  })
})



function openModal(modal, raceName, raceDate, raceInfo) {
    if (modal == null) return;

    document.getElementById('race-name').innerHTML= 'Race: ' + raceName;
    document.getElementById('race-date').innerHTML= 'Date: ' + raceDate;
    document.getElementById('race-distance').innerHTML= 'Distance: ' + raceInfo.distance + 'km';
    document.getElementById('race-departure-city').innerHTML= 'Departure city: ' + raceInfo.departure_city;
    document.getElementById('race-arrival-city').innerHTML= 'Arrival city: ' + raceInfo.arrival_city;

    if (raceInfo.classification.toLowerCase() == "unedefine" || raceInfo.classification.toLowerCase() == "undefined") {
        document.getElementById('race-classification').innerHTML= '';
    }
    else {
        document.getElementById('race-classification').innerHTML= 'Classification: ' + raceInfo.classification;
    }

    modal.classList.add('active');
}


function closeModal(modal) { 
    if (modal == null) return;
    modal.classList.remove('active');
}

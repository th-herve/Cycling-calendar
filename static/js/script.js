// source https://www.youtube.com/watch?v=MBaw_6cPmAw&t=184s
const openModalButtons = document.querySelectorAll('[data-modal-target]');
const closeModalButtons = document.querySelectorAll('[data-close-button]');


openModalButtons.forEach(button => {
  button.addEventListener('click', () => {
    const modal = document.querySelector(button.dataset.modalTarget);
    openModal(modal);
  })
})

closeModalButtons.forEach(button => {
  button.addEventListener('click', () => {
    const modal = button.closest('.modal');
    closeModal(modal);
  })
})


function openModal(modal, raceName, raceDate) {
  if (modal == null) return;
  document.getElementById('race-name').innerHTML= raceName;
  document.getElementById('race-date').innerHTML= raceDate;
  modal.classList.add('active');
}


function closeModal(modal) {
  if (modal == null) return;
  modal.classList.remove('active');
}

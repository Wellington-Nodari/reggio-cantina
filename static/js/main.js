/* taken from https://www.youtube.com/watch?v=SD7zspiPlQ4&t=186s */
const container = document.querySelector('.rating');
const items = container.querySelectorAll('.rating-item ')

container.onclick = e => {
    const elClass = e.target.classList;
    if (!elClass.contains('active')) {
        items.forEach(
            item => item.classList.remove('active')
        );
        console.log(e.target.getAttribute("data-rate"));
        elClass.add('active');
    }
};

let revF = document.getElementById('reviewForm');
let formC = document.getElementById('formDv');

    revF.addEventListener('click', () => {
    if (formC.style.display === 'none') {
      formC.style.display = 'block';
    } else {
      formC.style.display = 'none';
    }
    });


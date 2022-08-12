// For display the hidden form for write reviews

let revF = document.getElementById('reviewForm');
let formC = document.getElementById('formDv');

    revF.addEventListener('click', () => {
    if (formC.style.display === 'block') {
      formC.style.display = 'none';
    } else {
      formC.style.display = 'block';
    }
    });

// Handling the 5 stars selection for rating

const ratings = document.querySelectorAll('.rating');
ratings.forEach(rating =>
  rating.addEventListener('mouseleave', ratingHandler)
);

const stars = document.querySelectorAll('.rating .star');
stars.forEach(star => {
  star.addEventListener('mouseover', starSelection);
  star.addEventListener('mouseleave', starSelection);
  star.addEventListener('click', activeSelect);
});

function ratingHandler(e) {
  const childStars = e.target.children;
  for(let i = 0; i < childStars.length; i++) {
    const star = childStars.item(i)
    if (star.dataset.checked === "true") {
      star.classList.add('hover');
    }
    else {
      star.classList.remove('hover');
    }
  }
}

function starSelection(e) {
  const parent = e.target.parentElement
  const childStars = parent.children;
  const dataset = e.target.dataset;
  const note = +dataset.note; // Convert note (string) to note (number)
  for (let i = 0; i < childStars.length; i++) {
    const star = childStars.item(i)
    if (+star.dataset.note > note) {
      star.classList.remove('hover');
    } else {
      star.classList.add('hover');
    }
  }
}

function activeSelect(e) {
  const parent = e.target.parentElement
  const childStars = parent.children;
  const dataset = e.target.dataset;
  const note = +dataset.note;
  for (let i = 0; i < childStars.length; i++) {
    const star = childStars.item(i)
    if (+star.dataset.note > note) {
      star.classList.remove('hover');
      star.dataset.checked = "false";
    } else {
      star.classList.add('hover');
      star.dataset.checked = "true";
    }
  }

  const noteTextElement = parent.parentElement.lastElementChild.children.item(0)
  noteTextElement.innerText = `${note}`; document.getElementById("note").value = `${note}`;
}

// SlideShow for Reviews

let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("revDisp");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slides[slideIndex-1].style.display = "block";
}
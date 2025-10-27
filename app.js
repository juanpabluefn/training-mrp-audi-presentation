// Current slide state
let currentSlide = 1;
const totalSlides = 42;

// Initialize presentation
function init() {
  createNavDots();
  updatePresentation();
}

// Create navigation dots
function createNavDots() {
  const navDots = document.getElementById('navDots');
  navDots.innerHTML = '';
  
  for (let i = 1; i <= totalSlides; i++) {
    const dot = document.createElement('div');
    dot.className = 'nav-dot';
    if (i === currentSlide) {
      dot.classList.add('active');
    }
    dot.onclick = () => goToSlide(i);
    navDots.appendChild(dot);
  }
}

// Navigate to specific slide
function goToSlide(slideNumber) {
  if (slideNumber < 1 || slideNumber > totalSlides) return;
  
  // Remove active class from current slide
  const currentSlideEl = document.querySelector('.slide.active');
  if (currentSlideEl) {
    currentSlideEl.classList.remove('active');
  }
  
  // Update current slide number
  currentSlide = slideNumber;
  
  // Add active class to new slide
  const newSlideEl = document.querySelector(`[data-slide="${slideNumber}"]`);
  if (newSlideEl) {
    newSlideEl.classList.add('active');
  }
  
  // Update UI
  updatePresentation();
}

// Go to next slide
function nextSlide() {
  if (currentSlide < totalSlides) {
    goToSlide(currentSlide + 1);
  }
}

// Go to previous slide
function prevSlide() {
  if (currentSlide > 1) {
    goToSlide(currentSlide - 1);
  }
}

// Update presentation UI elements
function updatePresentation() {
  // Update navigation buttons
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  
  if (prevBtn) {
    prevBtn.disabled = currentSlide === 1;
  }
  
  if (nextBtn) {
    nextBtn.disabled = currentSlide === totalSlides;
  }
  
  // Update navigation dots
  const dots = document.querySelectorAll('.nav-dot');
  dots.forEach((dot, index) => {
    if (index + 1 === currentSlide) {
      dot.classList.add('active');
    } else {
      dot.classList.remove('active');
    }
  });
  
  // Update progress bar
  const progressBar = document.getElementById('progressBar');
  if (progressBar) {
    const progress = (currentSlide / totalSlides) * 100;
    progressBar.style.width = `${progress}%`;
  }
  
  // Scroll to top of slide content
  const activeSlide = document.querySelector('.slide.active');
  if (activeSlide) {
    const slideContent = activeSlide.querySelector('.slide-content');
    if (slideContent) {
      slideContent.scrollTop = 0;
    }
  }
}

// Keyboard navigation
document.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowRight' || event.key === 'PageDown') {
    nextSlide();
  } else if (event.key === 'ArrowLeft' || event.key === 'PageUp') {
    prevSlide();
  } else if (event.key === 'Home') {
    goToSlide(1);
  } else if (event.key === 'End') {
    goToSlide(totalSlides);
  }
});

// Touch support for mobile
let touchStartX = 0;
let touchEndX = 0;

document.addEventListener('touchstart', (event) => {
  touchStartX = event.changedTouches[0].screenX;
});

document.addEventListener('touchend', (event) => {
  touchEndX = event.changedTouches[0].screenX;
  handleSwipe();
});

function handleSwipe() {
  const swipeThreshold = 50;
  const diff = touchStartX - touchEndX;
  
  if (Math.abs(diff) > swipeThreshold) {
    if (diff > 0) {
      // Swipe left - next slide
      nextSlide();
    } else {
      // Swipe right - previous slide
      prevSlide();
    }
  }
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', init);
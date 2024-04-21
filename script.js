// Get references to the elements
const darkOverlay = document.querySelector('.dark-overlay');
const bottomImages = document.querySelectorAll('.bottom-image');
const image4 = document.querySelector('.image4');
const info1 = document.querySelector('.info1');
const info2 = document.querySelector('.info2');
const option = document.querySelector('.option'); // Replace with the appropriate selector for the option element

function handleClick(event) {
    // Show the dark overlay with a fade-in effect
    darkOverlay.style.display = 'block';
    setTimeout(() => {
        darkOverlay.style.opacity = '1';
    }, 50);

    // Play sound1 when clicking on bottom images 1 to 3
    const sound1 = new Audio('assets/sound1.ogg');
    sound1.play();

    // Show image4 with a fade-in effect
    image4.style.display = 'block';
    setTimeout(() => {
        image4.style.opacity = '1';
    }, 10);

    // Get the data-image attribute of the clicked image
    const clickedImage = event.target.getAttribute('data-image');

    // Check if image1 was clicked (data-image is '1')
    if (clickedImage === '1') {
        // Show info1 after a delay with a fade-in effect
        setTimeout(() => {
            info1.style.display = 'block';
            setTimeout(() => {
                info1.style.opacity = '1';
            }, 60);
        }, 400); // Adjust the delay (in milliseconds) as needed
    }
    if (clickedImage === '2') {
        // Show info1 after a delay with a fade-in effect
        setTimeout(() => {
            info2.style.display = 'block';
            setTimeout(() => {
                info2.style.opacity = '1';
            }, 160);
        }, 400); // Adjust the delay (in milliseconds) as needed
    }
}



function handleImage4Click(event) {
    // Hide info1/2 if it is visible
    if (info1.style.opacity === '1') {
        info1.style.opacity = '0';
        setTimeout(() => {
            info1.style.display = 'none';
        }, 300);
    }
    if (info2.style.opacity === '1') {
        info2.style.opacity = '0';
        setTimeout(() => {
            info1.style.display = 'none';
        }, 300);
    }

    // Hide image4 with a fade-out effect
    image4.style.opacity = '0';
    setTimeout(() => {
        image4.style.display = 'none';
    }, 300);

    // Hide the dark overlay with a fade-out effect
    darkOverlay.style.opacity = '0';
    setTimeout(() => {
        darkOverlay.style.display = 'none';
    }, 300);

    // Play sound2 when clicking on image4
    const sound2 = new Audio('assets/sound2.ogg');
    sound2.play();
}

function handleImageHover(event) {
    // Play sound3 when hovering over an image
    const sound3 = new Audio('assets/sound3.ogg');
    sound3.play();
}

bottomImages.forEach((image) => {
    image.addEventListener('click', handleClick);
    image.addEventListener('mouseover', handleImageHover); // Add hover event listener for each image
});

image4.addEventListener('click', handleImage4Click);

// Add event listener for option element hover
option.addEventListener('mouseover', handleOptionHover);

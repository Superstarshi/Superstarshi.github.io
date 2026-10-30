// parallax images
document.addEventListener('scroll', () => {
    const scrollY = window.scrollY;

    const grimdealer = document.querySelector('.grimdealer');
    const shrooms = document.querySelector('.daredevilshrooms');
    const logo = document.querySelector('.logo');

    if (!grimdealer || !shrooms) return;

    grimdealer.style.transform =
        `translate(-50%, ${scrollY * 0.2}px)`;

    shrooms.style.transform =
        `translate(-50%, ${scrollY * 0.15}px)`;

    if (logo) {
        logo.style.transform =
            `translate(-50%, ${scrollY * 0.1}px)`;
    }
});


const wrapper = document.querySelector('.parallax-wrapper');

window.addEventListener('scroll', () => {
    const scroll = window.scrollY;

    if (wrapper) {
        wrapper.style.transform =
            `translateX(-50%) translateY(${scroll * 0.2}px)`;
    }
});

if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual';
}



document.addEventListener('DOMContentLoaded', function () {
    console.log('Flash messages script loaded');
    const flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        console.log('Flash messages block found');
        setTimeout(() => {
            flashMessages.style.transition = 'opacity 0.5s';
            flashMessages.style.opacity = '0';
            setTimeout(() => {
                flashMessages.remove();
                console.log('Flash messages removed from DOM');
            }, 500);
        }, 3000);
    } else {
        console.log('Flash messages block NOT found');
    }
});

// Плавное исчезновение flash сообщений
document.addEventListener("DOMContentLoaded", () => {
    const flashMessages = document.querySelectorAll(".flash-message");
    if (flashMessages) {
        flashMessages.forEach((message) => {
            setTimeout(() => {
                message.style.transition = "opacity 0.5s";
                message.style.opacity = "0";
                setTimeout(() => {
                    message.remove();
                }, 500);
            }, 5000); // Убираем через 5 секунд
        });
    }
});

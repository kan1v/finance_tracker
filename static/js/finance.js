document.addEventListener('DOMContentLoaded', () => {
    // Кнопки показать/скрыть траты
    document.querySelectorAll('.toggle-expenses').forEach(button => {
        button.addEventListener('click', () => {
            const expensesList = button.closest('.category-block').querySelector('.expenses-list');
            if (expensesList.style.display === 'none' || expensesList.style.display === '') {
                expensesList.style.display = 'block';
                button.classList.add('rotate');
            } else {
                expensesList.style.display = 'none';
                button.classList.remove('rotate');
            }
        });
    });

    // Анимация пополнения баланса
    const balanceForm = document.getElementById('balance-form');
    const balanceValueElem = document.getElementById('balance-value');

    balanceForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const formData = new FormData(balanceForm);
        const addAmount = parseFloat(formData.get('add_balance'));
        if (isNaN(addAmount) || addAmount <= 0) return;

        // Запрос на сервер через fetch (AJAX), чтобы не перезагружать страницу
        fetch('/finance', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (response.redirected) {
                // Если сервер редиректит — обновим страницу
                window.location.href = response.url;
            }
        });

        // Красивая анимация прибавления суммы к балансу
        let currentBalance = parseFloat(balanceValueElem.textContent);
        let targetBalance = currentBalance + addAmount;
        let duration = 1000; // 1 секунда
        let startTime = null;

        function animate(time) {
            if (!startTime) startTime = time;
            let progress = time - startTime;
            let newBalance = currentBalance + (addAmount * (progress / duration));
            if (progress < duration) {
                balanceValueElem.textContent = newBalance.toFixed(2);
                requestAnimationFrame(animate);
            } else {
                balanceValueElem.textContent = targetBalance.toFixed(2);
            }
        }

        requestAnimationFrame(animate);

        // Очистить поле ввода
        balanceForm.querySelector('input[name="add_balance"]').value = '';
    });
});

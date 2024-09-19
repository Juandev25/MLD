document.addEventListener('DOMContentLoaded', () => {
    const tablero = Array(9).fill(' ');
    const celdas = document.querySelectorAll('.celda');

    celdas.forEach(celda => {
        celda.addEventListener('click', () => {
            const index = celda.id;

            if (tablero[index] === ' ') {
                // Movimiento del jugador
                tablero[index] = 'X';
                celda.textContent = 'X';

                // Verificar si el jugador ganó
                if (verificarGanador(tablero, 'X')) {
                    alert('¡Ganaste!');
                    return;
                }

                // Llamar a la IA
                fetch('/jugada', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ tablero: tablero }),
                })
                .then(response => response.json())
                .then(data => {
                    const movimientoIA = data.movimiento;
                    tablero[movimientoIA] = 'O';
                    document.getElementById(movimientoIA).textContent = 'O';

                    // Verificar si la IA ganó
                    if (verificarGanador(tablero, 'O')) {
                        alert('¡La IA ha ganado!');
                    }
                });
            }
        });
    });
});

// Función para verificar el ganador en el cliente
function verificarGanador(tablero, jugador) {
    const combinacionesGanadoras = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], // Filas
        [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columnas
        [0, 4, 8], [2, 4, 6]             // Diagonales
    ];
    return combinacionesGanadoras.some(combinacion => {
        return combinacion.every(index => tablero[index] === jugador);
    });
}

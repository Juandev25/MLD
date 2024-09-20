document.addEventListener('DOMContentLoaded', () => {
    let tablero = Array(9).fill(' ');
    const celdas = document.querySelectorAll('.celda');
    const reiniciarBtn = document.getElementById('reiniciar');
    const mensajeFinal = document.getElementById('mensaje-final');
    const mensajeTexto = document.getElementById('mensaje-texto');
    const modoTexto = document.getElementById('modo-texto');
    const selectorModo = document.querySelectorAll('input[name="modo"]');
    let modoActual = 'facil'; // Por defecto es fácil
    
    // Detectar cambios en el modo de juego
    selectorModo.forEach(radio => {
        radio.addEventListener('change', (event) => {
            modoActual = event.target.value;
            modoTexto.textContent = modoActual === 'facil' ? 'Fácil' : 'Difícil';
        });
    });

    celdas.forEach(celda => {
        celda.addEventListener('click', () => {
            const index = celda.id;

            if (tablero[index] === ' ') {
                // Movimiento del jugador
                tablero[index] = 'X';
                celda.innerHTML = '<span>X</span>';
                celda.classList.add('x');

                // Verificar si el jugador ganó
                if (verificarGanador(tablero, 'X')) {
                    mostrarMensaje('¡Ganaste!');
                    return;
                }

                // Verificar si hay empate
                if (verificarEmpate(tablero)) {
                    mostrarMensaje('¡Empate!');
                    return;
                }

                // Deshabilitar clics mientras la IA juega
                celdas.forEach(celda => celda.style.pointerEvents = 'none');

                // Llamar a la IA con un pequeño retraso
                setTimeout(() => {
                    fetch('/jugada', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ tablero: tablero, modo: modoActual }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        const movimientoIA = data.movimiento;
                        tablero[movimientoIA] = 'O';
                        const celdaIA = document.getElementById(movimientoIA);
                        celdaIA.innerHTML = '<span>O</span>';
                        celdaIA.classList.add('o');

                        // Verificar si la IA ganó
                        if (verificarGanador(tablero, 'O')) {
                            mostrarMensaje('¡La IA ha ganado!');
                            return;
                        }

                        // Verificar si hay empate después del movimiento de la IA
                        if (verificarEmpate(tablero)) {
                            mostrarMensaje('¡Empate!');
                            return;
                        }

                        // Volver a habilitar los clics
                        celdas.forEach(celda => celda.style.pointerEvents = 'auto');
                    });
                }, 500); // Añadir retraso para simular un movimiento más natural
            }
        });
    });

    // Función para reiniciar el juego
    reiniciarBtn.addEventListener('click', reiniciarJuego);

    function reiniciarJuego() {
        tablero = Array(9).fill(' ');
        celdas.forEach(celda => {
            celda.innerHTML = '';
            celda.classList.remove('x', 'o');
        });
        celdas.forEach(celda => celda.style.pointerEvents = 'auto');
        ocultarMensaje();
    }

    function mostrarMensaje(texto) {
        mensajeTexto.textContent = texto;
        mensajeFinal.classList.add('mostrar');
    }

    function ocultarMensaje() {
        mensajeFinal.classList.remove('mostrar');
    }

    function verificarEmpate(tablero) {
        return tablero.every(celda => celda !== ' ') && !verificarGanador(tablero, 'X') && !verificarGanador(tablero, 'O');
    }

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
});

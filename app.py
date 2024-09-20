from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import logging

# Configurar el nivel de logging para Flask
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Cargar los dos modelos
modelo_facil = load_model('tic_tac_toe_model_facil.h5')
modelo_dificil = load_model('tic_tac_toe_model_dificil.h5')

# Función para verificar si la IA puede ganar en su próximo movimiento
def verificar_si_puede_ganar(tablero, jugador):
    combinaciones_ganadoras = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Filas
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columnas
        [0, 4, 8], [2, 4, 6]             # Diagonales
    ]
    for combinacion in combinaciones_ganadoras:
        valores = [tablero[i] for i in combinacion]
        if valores.count(jugador) == 2 and valores.count(' ') == 1:
            return combinacion[valores.index(' ')]  # Retorna la posición ganadora
    return None

# Predecir el mejor movimiento según el modo de juego
def predecir_mejor_movimiento(tablero, modo):
    if modo == 'facil':
        modelo = modelo_facil
        logging.debug("Modo fácil seleccionado.")
    else:
        modelo = modelo_dificil
        logging.debug("Modo difícil seleccionado.")
        
        # Verificar si la IA puede ganar
        movimiento_para_ganar = verificar_si_puede_ganar(tablero, 'O')  # La IA es 'O'
        if movimiento_para_ganar is not None:
            logging.debug(f"Movimiento para ganar encontrado: {movimiento_para_ganar}")
            return movimiento_para_ganar

    movimientos_posibles = [i for i in range(9) if tablero[i] == ' ']
    mejor_valor = -float('inf')
    mejor_movimiento = None
    for movimiento in movimientos_posibles:
        tablero_temp = tablero.copy()
        tablero_temp[movimiento] = 'X'  # Simulamos el movimiento del jugador
        entrada_modelo = np.array([1 if x == 'X' else -1 if x == 'O' else 0 for x in tablero_temp]).reshape(1, -1)
        prediccion = modelo.predict(entrada_modelo)[0][0]
        logging.debug(f"Movimiento {movimiento}: Predicción {prediccion}")  # Verificar las predicciones
        if prediccion > mejor_valor:
            mejor_valor = prediccion
            mejor_movimiento = movimiento
    return mejor_movimiento

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jugada', methods=['POST'])
def jugada():
    data = request.json
    tablero = data['tablero']
    modo = data['modo']  # Obtener el modo de juego (fácil o difícil)
    
    logging.debug(f"Tablero recibido: {tablero}")
    logging.debug(f"Modo de juego recibido: {modo}")
    
    movimiento_ia = predecir_mejor_movimiento(tablero, modo)
    logging.debug(f"Movimiento IA seleccionado: {movimiento_ia}")
    
    return jsonify({'movimiento': movimiento_ia})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np

app = Flask(__name__)

# Cargar el modelo entrenado
modelo = load_model('tic_tac_toe_model.h5')

# Verifica si hay un ganador
def verificar_ganador(tablero, jugador):
    combinaciones_ganadoras = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
        [0, 4, 8], [2, 4, 6]              # Diagonales
    ]
    for combinacion in combinaciones_ganadoras:
        if tablero[combinacion[0]] == tablero[combinacion[1]] == tablero[combinacion[2]] == jugador:
            return True
    return False

# Predecir el mejor movimiento
def predecir_mejor_movimiento(tablero):
    movimientos_posibles = [i for i in range(9) if tablero[i] == ' ']
    mejor_valor = -float('inf')
    mejor_movimiento = None
    for movimiento in movimientos_posibles:
        tablero_temp = tablero.copy()
        tablero_temp[movimiento] = 'X'  # Simulamos el movimiento del jugador
        entrada_modelo = np.array([1 if x == 'X' else -1 if x == 'O' else 0 for x in tablero_temp]).reshape(1, -1)
        prediccion = modelo.predict(entrada_modelo)[0][0]
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
    movimiento_ia = predecir_mejor_movimiento(tablero)
    return jsonify({'movimiento': movimiento_ia})

if __name__ == '__main__':
    app.run(debug=True)

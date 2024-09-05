from flask import Flask, request, render_template
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import base64

# Cargar el modelo del generador
generator = tf.keras.models.load_model('generator_model.h5')

# Parámetros del modelo
latent_dim = 100
num_classes = 12  # Número de clases (frutas)

# Crear la aplicación Flask
app = Flask(__name__)

# Mapa de frutas (ajustar según tu dataset)
fruit_map = {
    0: 'aguaje',
    1: 'aguaymanto',
    2: 'granada',
    3: 'granadilla',
    4: 'mandarina',
    5: 'maracuya',
    6: 'naranja',
    7: 'piña',
    8: 'pitahaya',
    9: 'platanomorado',
    10: 'tangelo',
    11: 'tumbo'
}

# Ruta principal de la página web
@app.route('/')
def index():
    return render_template('index.html', fruit_map=fruit_map)

# Ruta para generar la imagen
@app.route('/generate', methods=['POST'])
def generate():
    fruit_name = request.form['fruit']
    
    # Obtener el índice de la fruta
    fruit_index = [key for key, value in fruit_map.items() if value == fruit_name][0]
    
    # Generar ruido aleatorio
    noise = np.random.normal(0, 1, (1, latent_dim))
    
    # Crear etiqueta de fruta (one-hot encoding)
    label = np.zeros((1, num_classes))
    label[0, fruit_index] = 1
    
    # Generar la imagen
    generated_image = generator.predict([noise, label])[0]
    generated_image = (generated_image * 127.5 + 127.5).astype(np.uint8)

    # Convertir la imagen a formato PNG para mostrar en la página web
    img = Image.fromarray(generated_image)
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    img_data = base64.b64encode(img_io.getvalue()).decode('ascii')

    return render_template('index.html', fruit_map=fruit_map, img_data=img_data)

if __name__ == '__main__':
    app.run(debug=True)

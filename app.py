from flask import Flask, render_template, request, send_file
import requests
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import io

app = Flask(__name__)

# URL para descargar el archivo desde Google Drive
file_id = 'YOUR_FILE_ID_HERE'
download_url = f"https://drive.google.com/file/d/1-B4QhXy4p-8sW1WZfxS_ivrGDneEllrj/view?usp=drive_link"

def download_model():
    response = requests.get(download_url)
    model_path = "generator_model.h5"
    with open(model_path, "wb") as f:
        f.write(response.content)
    return model_path

# Descargar el modelo al iniciar la aplicación
model_path = download_model()
generator = load_model(model_path)

def text_to_label(text):
    fruit_names = ['manzana', 'platano', 'naranja', 'pera', 'uva', 'fresa', 'cereza', 'piña', 'mango', 'kiwi', 'limon', 'sandia']
    if text.lower() in fruit_names:
        index = fruit_names.index(text.lower())
        label = np.zeros((1, len(fruit_names)))
        label[0, index] = 1
        return label
    else:
        raise ValueError("Fruta no reconocida")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_image', methods=['GET'])
def generate_image():
    fruit_name = request.args.get('name')
    label_one_hot = text_to_label(fruit_name)
    noise = np.random.normal(0, 1, (1, 100))
    generated_image = generator.predict([noise, label_one_hot])[0]
    generated_image = (generated_image * 127.5 + 127.5).astype(np.uint8)

    img = Image.fromarray(generated_image)
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, render_template, url_for
from rembg import remove
import os

app = Flask(__name__)

# Папка для загрузки и обработки изображений
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'static/processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Убедимся, что папки существуют
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return "No file uploaded", 400

    # Получаем загруженный файл
    image_file = request.files['image']
    filename = image_file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Сохраняем файл в папку uploads
    image_file.save(filepath)

    # Открываем изображение и удаляем фон
    with open(filepath, "rb") as image_data:
        output = remove(image_data.read())

    # Сохраняем обработанный файл в static/processed
    processed_filename = f"processed_{filename}.png"
    processed_filepath = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
    with open(processed_filepath, "wb") as processed_file:
        processed_file.write(output)

    # Путь к загруженному изображению и обработанному
    uploaded_image_url = url_for('static', filename=f'uploads/{filename}')
    processed_image_url = url_for('static', filename=f'processed/{processed_filename}')

    # Передаем оба пути в шаблон
    return render_template('index.html', uploaded_image_url=uploaded_image_url, image_url=processed_image_url)

if __name__ == '__main__':
    app.run(debug=True)

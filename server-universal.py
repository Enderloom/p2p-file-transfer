import os
import time
from flask import Flask, request, send_from_directory
from threading import Thread

# Server parametrləri
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Faylları saxlayacaq qovluğu yoxlayır
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Faylları silmək üçün fon prosesi
def file_cleanup():
    while True:
        for file in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, file)
            if time.time() - os.path.getmtime(file_path) > 600:
                os.remove(file_path)
        time.sleep(60)  # Hər 60 saniyədə bir yoxla

Thread(target=file_cleanup, daemon=True).start()

# Fayl yükləmə
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Fayl tapılmadı", 400
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return "Fayl yükləndi", 200

# Fayl siyahısı
@app.route('/list', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return {"files": files}, 200

# Fayl yükləmə
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == "__main__":
    import socket
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"Server başladıldı: {ip_address}:8080")
    app.run(host=ip_address, port=8080)

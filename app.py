from flask import Flask
from database.db import init_db
from routes.upload_route import upload_bp
from routes.download_route import download_bp
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

init_db()

app.register_blueprint(upload_bp, url_prefix='/uploads')
app.register_blueprint(download_bp, url_prefix='/downloads')


@app.route('/')
def index():
    return {
        "mensagem": "API de upload e download no ar!",
        "rotas": {
            "upload": "POST /uploads/upload (campo 'file')",
            "download": "GET /downloads/<nome_do_arquivo>"
        }
    }


# Só roda ao executar "python app.py" (desenvolvimento local).
# No Render, quem inicia a aplicação é o gunicorn (veja o README).
if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')

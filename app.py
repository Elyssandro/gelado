from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/baixar', methods=['POST'])
def baixar():
    url = request.form.get('url')
    tipo = request.form.get('tipo')
    qualidade = request.form.get('qualidade')
    
    # Configurações do yt-dlp para baixar o arquivo
    ydl_opts = {}

    if tipo == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioquality': '0',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }
    elif tipo == 'mp4':
        ydl_opts = {
            'format': f'bestvideo[height<={qualidade}]+bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }

    # Baixar o vídeo/música usando yt-dlp
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return f'Arquivo de {tipo} baixado com sucesso!'
    except Exception as e:
        return f'Erro ao baixar o vídeo: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from utils import converter, sintetizador, afinador, extras

UPLOAD_FOLDER = 'static/audio'
ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'm4a'}
ALLOWED_TEXT_EXTENSIONS = {'txt', 'abc', 'ly'}

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Verifica extensões permitidas
def allowed_file(filename, allowed_set):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_set

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processar', methods=['GET', 'POST'])
def processar():
    if request.method == 'GET':
        return render_template('processar.html')

    inicio = time.time()  # ⏱️ Início da contagem de tempo

    texto_partitura = request.form.get('partitura')
    instrumento = request.form.get('instrumento', 'piano')
    audio = request.files.get('audio')

    nome_base = str(uuid.uuid4())
    caminho_saida = os.path.join(app.config['UPLOAD_FOLDER'], f'{nome_base}.wav')
    tipo_entrada = None

    try:
        if audio and allowed_file(audio.filename, ALLOWED_AUDIO_EXTENSIONS):
            filename = secure_filename(audio.filename)
            caminho_audio = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            audio.save(caminho_audio)
            tipo_entrada = "voz"

            print(f"📥 Salvando áudio em: {caminho_audio}")
            print("🎛️ Corrigindo voz...")
            afinador.corrigir_voz(caminho_audio, caminho_saida)

        elif texto_partitura and len(texto_partitura.strip()) > 0:
            tipo_entrada = "partitura"
            midi_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{nome_base}.mid')

            print("✍️ Convertendo texto para MIDI...")
            converter.texto_para_midi(texto_partitura, midi_path)

            print(f"🎹 Gerando áudio com instrumento: {instrumento}")
            sintetizador.midi_para_audio(midi_path, caminho_saida, instrumento)

        else:
            flash("Por favor, envie um áudio ou escreva uma melodia.")
            return redirect(url_for('processar'))

        print("🎧 Aplicando pós-processamento...")
        extras.pos_processamento(caminho_saida)

        duracao = time.time() - inicio
        print(f"✅ Música gerada em {duracao:.2f} segundos.")

        return redirect(url_for('resultado', filename=f'{nome_base}.wav', origem=tipo_entrada))

    except Exception as e:
        flash(f"Ocorreu um erro: {str(e)}")
        return redirect(url_for('processar'))


@app.route('/resultado')
def resultado():
    filename = request.args.get('filename')
    origem = request.args.get('origem')
    return render_template('resultado.html', filename=filename, origem=origem)

@app.route('/baixar/<filename>')
def baixar(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)

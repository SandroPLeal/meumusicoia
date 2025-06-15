import librosa
import numpy as np
from pydub import AudioSegment

def corrigir_voz(caminho_entrada, caminho_saida):
    """
    Corrige imperfeições básicas de afinação aplicando quantização de pitch.
    """
    print(f"[🎤] Corrigindo voz: {caminho_entrada}")

    # Carrega o áudio e extrai pitch
    y, sr = librosa.load(caminho_entrada)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

    # Média dos pitches dominantes
    pitch_values = []
    for i in range(pitches.shape[1]):
        index = magnitudes[:, i].argmax()
        pitch = pitches[index, i]
        if pitch > 0:
            pitch_values.append(pitch)

    if not pitch_values:
        print("[!] Nenhum pitch detectado. Mantendo áudio original.")
        audio = AudioSegment.from_file(caminho_entrada)
        audio.export(caminho_saida, format="wav")
        return

    # Calcular média e ajustar tom geral
    media_pitch = np.median(pitch_values)
    print(f"[i] Pitch médio: {media_pitch:.2f} Hz")

    # Alvo mais próximo (nota padrão em Hz)
    notas_padrao = np.array([
        261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88  # C4–B4
    ])
    destino = notas_padrao[np.argmin(np.abs(notas_padrao - media_pitch))]
    semitons = 12 * np.log2(destino / media_pitch)
    print(f"[✓] Corrigindo em {semitons:.2f} semitons → {destino:.2f} Hz")

    # Aplicar transposição (com pydub)
    audio = AudioSegment.from_file(caminho_entrada)
    audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * 2.0**(semitons / 12.0))
    }).set_frame_rate(audio.frame_rate)

    audio.export(caminho_saida, format="wav")
    print(f"[✓] Voz afinada salva em: {caminho_saida}")

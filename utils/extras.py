from pydub import AudioSegment, effects
import os

def pos_processamento(caminho_wav, aplicar_fade=True, cortar_silencio=True):
    """
    Aplica normalização, cortes e fades no áudio final.
    """
    print(f"[🔧] Pós-processando: {caminho_wav}")
    try:
        audio = AudioSegment.from_file(caminho_wav, format="wav")

        # Normalização
        audio = effects.normalize(audio)
        print("✔ Áudio normalizado")

        # Cortar silêncios (simples)
        if cortar_silencio:
            audio = strip_silence(audio)
            print("✔ Silêncio cortado")

        # Aplicar fade-in/out
        if aplicar_fade:
            audio = audio.fade_in(500).fade_out(800)
            print("✔ Fade aplicado")

        # Salvar de volta
        audio.export(caminho_wav, format="wav")
        print("✔ Arquivo final salvo com sucesso")

    except Exception as e:
        print(f"[!] Erro ao processar áudio: {e}")

def strip_silence(audio, threshold_db=-45.0, chunk_ms=10):
    """
    Remove silêncio do início e fim com base no limiar de volume.
    """
    def detect_leading_silence(sound):
        trim_ms = 0
        while trim_ms < len(sound) and sound[trim_ms:trim_ms+chunk_ms].dBFS < threshold_db:
            trim_ms += chunk_ms
        return trim_ms

    start_trim = detect_leading_silence(audio)
    end_trim = detect_leading_silence(audio.reverse())
    return audio[start_trim:len(audio) - end_trim]

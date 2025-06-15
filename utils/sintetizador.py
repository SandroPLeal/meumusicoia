import os
import subprocess

def midi_para_audio(midi_path, output_wav_path, instrumento='piano'):
    """
    Converte um arquivo MIDI para WAV usando FluidSynth e um SoundFont.
    """
    # Caminho do SoundFont (.sf2)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    soundfont_path = os.path.join(base_dir, 'soundfonts', 'FluidR3_GM.sf2')

    if not os.path.exists(soundfont_path):
        raise FileNotFoundError(f"SoundFont não encontrado: {soundfont_path}")

    # Comando para usar o FluidSynth
    cmd = [
        "fluidsynth",
        "-ni",
        soundfont_path,
        midi_path,
        "-F", output_wav_path,
        "-r", "44100"
    ]

    print(f"[▶] Gerando áudio com FluidSynth: {output_wav_path}")
    subprocess.run(cmd, check=True)
    print(f"[✓] WAV gerado com sucesso: {output_wav_path}")

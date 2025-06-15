from music21 import stream, note, midi

def texto_para_midi(texto, caminho_saida):
    """
    Converte uma sequência de notas em texto para um arquivo MIDI.
    Exemplo de entrada: "C4 D4 E4 G4 A4"
    """
    melodia = stream.Stream()
    duracao = 1.0  # Cada nota tem 1 tempo (semínima)

    notas = texto.strip().split()

    for nome in notas:
        try:
            n = note.Note(nome)
            n.quarterLength = duracao
            melodia.append(n)
        except Exception as e:
            print(f"Erro ao interpretar nota '{nome}': {e}")

    mf = midi.translate.streamToMidiFile(melodia)
    mf.open(caminho_saida, 'wb')
    mf.write()
    mf.close()
    print(f"[✓] MIDI gerado em: {caminho_saida}")

from pathlib import Path

def shift_pitch(audio_path: str, output_path: str, semitones: int):
    import librosa
    import soundfile as sf

    # Load the audio
    y, sr = librosa.load(audio_path, sr=None)

    # Shift the pitch
    y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=semitones)

    # Save the output
    sf.write(output_path, y_shifted, sr)

def create_audio_all_keys(audio_path: str | Path, output_folder: str, original_key: str = "C"):
    import librosa
    import soundfile as sf
    import os
    from pathlib import Path
    from music21 import pitch

    audio_path = Path(audio_path)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    # Load original audio
    y, sr = librosa.load(audio_path, sr=None)

    # Get semitone shifts from original key to all 12 keys
    all_keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    original_pitch = pitch.Pitch(original_key)

    for key in all_keys:
        target_pitch = pitch.Pitch(key)
        semitone_shift = target_pitch.midi - original_pitch.midi

        # Pitch shift
        y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=semitone_shift)

        # Save file
        out_path = output_folder / f"{key}.wav"
        sf.write(out_path, y_shifted, sr)

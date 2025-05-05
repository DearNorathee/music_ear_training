from pathlib import Path
from typing import Union

def shift_pitch(audio_path: str, output_path: str, semitones: int):
    import librosa
    import soundfile as sf

    # Load the audio
    y, sr = librosa.load(audio_path, sr=None)

    # Shift the pitch
    y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=semitones)

    # Save the output
    sf.write(output_path, y_shifted, sr)

def create_audio_all_keys(audio_path: Union[str , Path], output_folder: str, original_key:str):
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

# is it possible for me to break it down how to play it in piano?
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.audio import load_audio
from basic_pitch.note_creation import notes_to_midi, output_notes_to_midi

audio_path = "piano_audio.wav"
audio, sr = load_audio(audio_path)
model_output = predict(audio, sr, model_path=ICASSP_2022_MODEL_PATH)

# Convert to list of notes (start time, end time, pitch)
notes = model_output["notes"]
for note in notes:
    print(f"Pitch: {note[2]}, Start: {note[0]:.2f}s, End: {note[1]:.2f}s")


def test_shift_pitch():
    audio_path01 = r"C:\C_Music\Healing Songs\01 Tears of Gold.mp3"
    output_path01 = r"C:\C_Video_Python\riff_music\01 Tears of Gold_B.mp3"
    shift_pitch(audio_path01,output_path01,3)

test_shift_pitch()
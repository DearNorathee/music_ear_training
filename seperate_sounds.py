from spleeter.separator import Separator

def separate_vocals(audio_path: str, output_folder: str):
    from pathlib import Path
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Load 2-stem model (vocals + accompaniment)
    separator = Separator('spleeter:2stems')  # Requires pretrained models

    # Perform separation
    separator.separate_to_file(audio_path, output_folder)

# Demucs

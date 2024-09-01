# use env => latest python
from music21 import chord
import music21.note
import musicpy as mp
from typing import Literal, Union, Any, List
from mingus.core import scales, notes
from pathlib import Path
# import mingus.core

import sys
sys.path.append(r"C:\Users\Heng2020\OneDrive\D_Code\Python\Python Music\2024\01 Lego Riff Creation\lego_riff_creation")
import music_func as mus
import pandas as pd

ScaleType = Union[scales._Scale,Literal["Major","Minor","Natural minor","Ionian","Dorian","Phrygian","Lydian","Mixolydian","Aeolian","Locrian","Harmonic minor","Melodic minor","Whole tone","Chromatic"]]
ALL_KEYS = ["C","D","E","F","G","A","B", "C#","D#","Gb","Ab","Bb"]



def get_chord_notes(
        start_note:str
        ,chord_type:str = "maj"
        ,return_type:Literal["str","music21.note"] = "str"
        ) -> Union[List[str],List[music21.note.Note]]:
    # medium tested
    import musicpy as mp
    import music21.note
    # Create a chord object
    chord_notes = mp.get_chord(start_note,chord_type).notes
    
    # Get the pitch names (notes) of the chord
    notes = [str(note) for note in chord_notes]
    notes_music21 = [music21.note.Note(note) for note in notes]
    if return_type == "str":
        return notes
    elif return_type == "music21.note":
        return notes_music21

def tranpose_by_key(
    original_notes: List[str]
    ,from_key: str
    ,to_key: str
    ,from_scale_type: ScaleType = "Major"
    ,to_scale_type: ScaleType = "Major"
    ,return_type:Literal["str","music21.note"] = "str"
) -> List[str]:
    # medium tested
    import music21.note
    from music21 import interval
    from mingus.core import intervals
    # Helper function to get the appropriate scale object
    def get_scale(key: str, scale_type: ScaleType) -> scales._Scale:
        if isinstance(scale_type, scales._Scale):
            return scale_type(key)
        elif isinstance(scale_type, str):
            scale_type = scale_type.lower()
            if scale_type == "major":
                return scales.Major(key)
            elif scale_type in ["minor", "natural minor"]:
                return scales.NaturalMinor(key)
            else:
                raise ValueError(f"Unsupported scale type string: {scale_type}")
        else:
            raise TypeError(f"Unsupported scale type: {type(scale_type)}")

    # Create the scales
    from_scale = get_scale(from_key, from_scale_type)
    to_scale = get_scale(to_key, to_scale_type)
    
    # Get the notes for the given scale degrees in the original scale
    original_notes_obj:List[music21.note.Note]
    original_notes_obj = [music21.note.Note(note) for note in original_notes]
    # Find the interval between the two keys
    # interval.Interval()
    interval_between_key = intervals.determine(from_key, to_key)
    

    # Transpose each note
    # for note in original_notes_obj:
    #     note.transpose()

    # try to fix error from .transpose
    if interval_between_key in ["major unison"]:
        interval_between_key = 0
    elif interval_between_key in ['minor fifth']:
        interval_between_key = 6


    transposed_notes_obj = [note.transpose(interval_between_key) for note in original_notes_obj]
    transposed_notes_str = [note.nameWithOctave for note in transposed_notes_obj]
    # transposed_notes_str = [note._setOctave() for note in transposed_notes_obj]
    # Convert transposed notes to scale degrees in the new scale
    # new_scale_degrees = [to_scale.determine(note)[0] + 1 for note in transposed_notes]
    if return_type in ["music21.note"]:
        return transposed_notes_obj
    elif return_type in ["str"]:
        return transposed_notes_str


def tranpose_by_interval(
    original_notes: List[int]
    ,interval:int
    ,return_type:Literal["str","music21.note"] = "str"
) -> List[str]:
    # not done yet
    """
    interval is semi note
    """
    import music21.note
    # Helper function to get the appropriate scale object

    
    # Get the notes for the given scale degrees in the original scale
    original_notes_obj:List[music21.note.Note]
    original_notes_obj = [music21.note.Note(note) for note in original_notes]


    transposed_notes_obj = [note.transpose(interval) for note in original_notes_obj]
    transposed_notes_str = [note.nameWithOctave for note in transposed_notes_obj]
    # transposed_notes_str = [note._setOctave() for note in transposed_notes_obj]
    # Convert transposed notes to scale degrees in the new scale
    # new_scale_degrees = [to_scale.determine(note)[0] + 1 for note in transposed_notes]
    if return_type in ["music21.note"]:
        return transposed_notes_obj
    elif return_type in ["str"]:
        return transposed_notes_str


def create_melody(
    notes: List[str],
    in_key: str,
    out_keys: List[str] = ALL_KEYS,
    octaves: List[int] = [1, 2, 3, 4, 5, 6, 7]
) -> pd.DataFrame:
    # medium tested
    # need better name
    """
    the objective of this function is to generate notes in different keys and octaves
    notes must contain octave as num !!! 
    """
    import py_string_tool as pst
    from music21 import chord, pitch
    
    melody_data = []

    # Loop over each key and octave
    for key in out_keys:
        for octave in octaves:
            transposed_notes = []
            for note in notes:
                n = pitch.Pitch(note)
                n.octave = octave
                transposed_notes.append(tranpose_by_key([n], in_key, key)[0])
            
            melody_data.append({
                'Key': key,
                'Octave': octave,
                'Notes': transposed_notes
            })

    # Create DataFrame
    df = pd.DataFrame(melody_data)

    # Sort by Octave, then Key
    df = df.sort_values(by=['Octave', 'Key']).reset_index(drop=True)

    return df

def create_midi_melody(
    notes: List[str],
    in_key: str,
    prefix_name:str,
    output_folder:Union[str,Path],
    out_keys: List[str] = ALL_KEYS,
    octaves: List[int] = [1, 2, 3, 4, 5, 6, 7],
    longer_last_note:int = 4,
    outname_key_before_octave:bool = True
    ) -> None:
    # medium tested
    # need better name
    def _create_midi_melody_H1(
            notes,
            key,
            octave, 
            longer_last_note:int = 4,
            outname_key_before_octave:bool = True):
        """
        outname_key_before_octave if True used to generate filename using key before octave: "Key D_Octave 3"
            if False "Octave 3_Key D"
        """

        # helper function to generate files using pd.DataFrame
        if outname_key_before_octave:
            curr_out_name = f"{prefix_name}_Key {key}_Octave {octave}.mid"
        else:
            curr_out_name = f"{prefix_name}_Octave {octave}_Key {key}.mid"

        curr_out_path = Path(str(output_folder)) / curr_out_name
        note_lengths = [1 for _ in range(len(notes))]
        note_lengths[-1] = longer_last_note
        mus.create_midi(curr_out_path,notes,note_lengths=note_lengths)

    melody_df = create_melody(notes, in_key, out_keys, octaves)
    melody_df.apply(
        lambda row: _create_midi_melody_H1(row['Notes'],row['Key'],row['Octave'],longer_last_note,outname_key_before_octave), axis=1
    )


# need better name
# ---------------------------------------------------------------------------
def test_get_chord_notes():
    actual01 = get_chord_notes("A")
    expect01 = ['A4', 'C#5', 'E5']
    assert actual01 == expect01

def test_tranpose_by_key():
    actual01 = tranpose_by_key(["C","E","G"],"C","D")
    actual02 = tranpose_by_key(["A4","C#5","E5"],"A","C")

    expect01 = ['D', 'F#', 'A']
    expect02 = ['C5', 'E5', 'G5']
    # print(actual01)
    print(actual02)
    assert actual01 == expect01

def main():
    main_test()

def main_test():
    test_tranpose_by_key()
    test_get_chord_notes()


if __name__ == "__main__":
    main()




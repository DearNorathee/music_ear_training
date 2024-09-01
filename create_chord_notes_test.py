from create_chord_notes import *
from pandas.testing import assert_frame_equal
from pathlib import Path

project_folder = Path(__file__).parent
test_output_folder = project_folder / "test_output"
test_01_triad_folder = test_output_folder / "01 Triads"

def test_create_melody():
    notes = ["C3", "E3", "G3"]
    out_keys = ["C", "G", "A"]
    octaves = [1, 4, 6]

    actua01 = create_melody(notes, in_key="C", out_keys=out_keys, octaves=octaves)

    expect01_dict = \
    {
        'Key': ['A', 'C', 'G', 'A', 'C', 'G', 'A', 'C', 'G'],
        'Octave': [1, 1, 1, 4, 4, 4, 6, 6, 6],
        'Notes': [
                ['A1', 'C#2', 'E2'],
                ['C1', 'E1', 'G1'],
                ['G1', 'B1', 'D2'],
                ['A4', 'C#5', 'E5'],
                ['C4', 'E4', 'G4'],
                ['G4', 'B4', 'D5'],
                ['A6', 'C#7', 'E7'],
                ['C6', 'E6', 'G6'],
                ['G6', 'B6', 'D7']
                ]
    }

    # print(actua01)
    expect01 = pd.DataFrame(expect01_dict)
    assert_frame_equal(actua01, expect01)

def test_create_midi_melody():
    project_folder = Path(__file__).parent
    test_output_folder = project_folder / "test_output"
    notes = ["C3", "E3", "G3"]
    create_midi_melody(notes, in_key="C", prefix_name="Triad", output_folder=test_01_triad_folder)

def arpeggio_02_minor_triads():
    output_folder = r"C:\Users\Heng2020\OneDrive\Desktop\Musical Notes Collection\Listening Practice\Arpeggio\03 Minor Triads Up"
    notes = ["C3", "Eb3", "G3"]
    create_midi_melody(notes, in_key="C", prefix_name="Minor Triad", output_folder=output_folder)

arpeggio_02_minor_triads()
# test_create_midi_melody()
# test_create_melody()
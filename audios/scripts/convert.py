from pydub import AudioSegment, effects


def normalize():
    sound_files = [
        ("1.m4a", "1.mp3"),
        ("2.m4a", "2.mp3"),
        ("3.m4a", "3.mp3"),
        ("4.m4a", "4.mp3"),
        ("5.m4a", "5.mp3"),
    ]
    OUTPUT_DIR = "../"
    INPUT_DIR = "../"

    for (f_in, f_out) in sound_files:
        rs = AudioSegment.from_file(f"{INPUT_DIR}{f_in}", f_in.split(".")[-1])
        normalized = effects.normalize(rs)
        normalized.export(f"{OUTPUT_DIR}{f_out}", format=f_out.split(".")[-1])


def apply_gain():
    TARGET_DBFS = -20.0
    file = "1"

    sound = AudioSegment.from_file(f"{file}.m4a", "m4a")
    normalized = sound.apply_gain(TARGET_DBFS - sound.dBFS)
    normalized.export(f"{file}.mp3", format="mp3")


normalize()

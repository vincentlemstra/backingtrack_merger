import os
import glob
from pydub import AudioSegment
from pydub.utils import mediainfo


tracks = glob.glob(os.path.expanduser(
    "~/Music/backingtracks/tracks/*.m4a"))  # get all .m4a files

setup_track = AudioSegment.from_file(os.path.expanduser(
    "~/Music/backingtracks/tracks/Click Track.m4a"), format="m4a")

base_segment = AudioSegment.silent(
    duration=len(setup_track))  # set empty track

setup_bitrate = mediainfo(os.path.expanduser(
    "~/Music/backingtracks/tracks/Click Track.m4a"))["bit_rate"]  # setup bitrate


for track in tracks:
    audio = AudioSegment.from_file(track, format="m4a")  # extract m4a audio
    base_segment = base_segment.overlay(audio)  # overlay audio

file_handle = base_segment.export(os.path.expanduser(
    "~/Music/backingtracks/combined/tracks_combined.mp3"),
    format="mp3", bitrate=setup_bitrate)  # export combined file

print('Conversion Complete')

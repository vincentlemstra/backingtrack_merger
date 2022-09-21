import os
import glob
from pydub import AudioSegment
from pydub.utils import mediainfo


def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply == 'y':
            return True
        if reply == 'n':
            return False
        else:
            print('Please answer with (y/n: ')


# user inputs:
title = input("Song title: ")
artist = input("Song artist: ")
drumless = yes_or_no("Drumless track?")


tracks = glob.glob(os.path.expanduser(
    "~/Music/backingtracks/tracks/*.m4a"))  # get all .m4a files


if drumless: 
    tracks.remove(os.path.expanduser(
        "~/Music/backingtracks/tracks/Drums (Live).m4a")) #exclude drums .m4a file


setup_track = AudioSegment.from_file(os.path.expanduser(
    "~/Music/backingtracks/tracks/Click Track.m4a"), format="m4a") # basis track for setup

base_segment = AudioSegment.silent(
    duration=len(setup_track))  # set empty track

setup_bitrate = mediainfo(os.path.expanduser(
    "~/Music/backingtracks/tracks/Click Track.m4a"))["bit_rate"]  # setup bitrate

for track in tracks:
    audio = AudioSegment.from_file(track, format="m4a")  # extract m4a audio
    base_segment = base_segment.overlay(audio)  # overlay audio


filename = (f"{title} - {artist} - All") # filename for export

if drumless:
    filename = (f"{title} - {artist} - Drumless") # filename drumless for export


file_handle = base_segment.export(os.path.expanduser(f"~/Music/backingtracks/combined/{filename}.mp3"),
                                  format="mp3", bitrate=setup_bitrate)  # export combined file

print('Conversion Complete')

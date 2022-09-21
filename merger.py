import os
import glob
from pydub import AudioSegment
from pydub.utils import mediainfo

# m4a_files = glob.glob(os.path.expanduser("~/Desktop/MULTITRACKS/*.m4a"))  # get all .m4a files
# print(m4a_files)

# for wav_file in wav_files:
#     mp3_file = os.path.splitext(wav_file)[0] + '.mp3' # rename to .mp3
#     # print(mp3_file)
#     sound = pydub.AudioSegment.from_wav(wav_file) # extract wav audio
#     sound.export(mp3_file, format='mp3') # export into mp3 format
#     # os.remove (wav_file)

# print('Conversion Complete')


# wav_files = glob.glob("./multitrack_files/*.wav")
# print(wav_files) # You can use this to get a list -> get individual items by looping (instead of sound1 + sound2)

sound1 = AudioSegment.from_file(os.path.expanduser("~/Desktop/MULTITRACKS/Click Track.m4a"), format="m4a")
# sound2 = AudioSegment.from_file(os.path.expanduser("~/Desktop/MULTITRACKS/Guide.m4a"), format="m4a")
sound3 = AudioSegment.from_file(os.path.expanduser("~/Desktop/MULTITRACKS/Drums (Live).m4a"), format="m4a")

bitrate = mediainfo(os.path.expanduser("~/Desktop/MULTITRACKS/Click Track.m4a"))["bit_rate"]

base_segment = AudioSegment.silent(duration=len(sound1))

combined = base_segment.overlay(sound1)

file_handle = combined.export("./combined_files/combined.mp3", format="mp3", bitrate=bitrate)
print('Conversion Complete') 
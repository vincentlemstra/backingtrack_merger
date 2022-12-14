import os
import glob
import tqdm
import argparse

from pydub import AudioSegment
from pydub.utils import mediainfo
import yaml
from yaml import CSafeLoader as SafeLoader

class Merger:
    name = ""
    tracks = []
    folder = ""
    config_file = ""
    config = {}
    def __init__(self, folder, config_file):
        self.folder = folder
        self.name = os.path.basename(folder)
        self.config = yaml.load(open(config_file, 'r'), Loader=SafeLoader)["Merger"]
        if self.config["tracks_suffix_folder"]:
            self.tracks =  glob.glob(os.path.expanduser(folder) + f"/{self.config['tracks_suffix_folder']}" + f"/*.{self.config['format']}")
        else:
            self.tracks =  glob.glob(os.path.expanduser(folder) + f"/*.{self.config['format']}")



    def merge(self):
        if len(self.tracks) == 0:
            raise Exception("Couldn't find any tracks in the folder")
        setup_track = AudioSegment.from_file(self.tracks[0], format=self.config["format"])  # basis track for setup

        base_segment = AudioSegment.silent(
            duration=len(setup_track))  # set empty track

        for track in tqdm.tqdm(self.tracks, position=1, desc=f"Generating track {self.name}"):
            track_name = os.path.basename(track).lower()

            track_name = track_name.replace(f".{self.config['format']}", "")
            track_name = track_name.replace(" ", "_")

            track = AudioSegment.from_file(track, format=self.config['format'])
            config_track = self.config["tracks"][track_name] if track_name in self.config["tracks"] else self.config["tracks"]["default"]

            if not config_track["include"]:
                    continue
            track = track + config_track["level"]
            base_segment = base_segment.overlay(track)
        filename = self.name  # filename for export
        if "title-prefix" in self.config:
            filename = f"{self.config['title-prefix']} - {filename}"
        if "title-suffix" in self.config:
            filename = f"{filename} - {self.config['title-suffix']}"

        setup_bitrate = mediainfo(self.tracks[0])["bit_rate"]
        if "output_folder" in self.config:
            base_segment.export(os.path.expanduser(self.config["output_folder"]) + f"/{filename}.{self.config['output_format']}", format=self.config["output_format"], bitrate=setup_bitrate)
        else:
            base_segment.export(os.path.expanduser(f"{self.folder}/{filename}.{self.config['output_format']}"),
                format=self.config["output_format"], bitrate=setup_bitrate) # export combined file


if __name__=="__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional argument
    parser.add_argument("-f", "--folder", help = "Folder with folders that have tracks", required=True)
    parser.add_argument("-c", "--config", help = "Config file", required=True)
    
    # Read arguments from command line
    args = parser.parse_args()
    
    subfolders = [ f.path for f in os.scandir(args.folder) if f.is_dir() ]
    for folder in subfolders:
        try:
            merger = Merger(folder, args.config)

            merger.merge()
        except Exception as e:
            print(e)
            print("Failed to merge " + folder)

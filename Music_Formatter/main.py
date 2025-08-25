import eyed3
import os
import sys


dir = sys.argv[1]
artist = input("Artist Name: ")
album =  input("Album Name: ")

songs = []

def main():       
    for filename in os.listdir(dir):
        if not filename.endswith("jpg"):
            file_path = os.path.join(dir,filename)
            mp3 = eyed3.load(file_path)
            if mp3.tag:
                if artist != '':
                    mp3.tag.artist = artist
                mp3.tag.title = filename
                if album != '':
                    mp3.tag.album = album
                track_num = input("{} is track: ".format(filename))
                mp3.tag.track_num = track_num
                mp3.tag.save()
   

if __name__ == "__main__":
    main()
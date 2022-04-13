import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from os import path
from pygame import mixer
from twodxPlay.twodx import Twodx
import sys, traceback
from datetime import timedelta
import struct
import argparse

version='V1.0.1'

parser = argparse.ArgumentParser(description='A command line app for playing and extracting konami 2dx audio files.')
parser.add_argument('infile')
parser.add_argument('-e', '--extract', nargs='?', const='all', help='Extract the wav files. Optionally specify a number, a comma-separated list of numbers or a range such as 10-20.'
                                            ' Don\'t use spaces, and NOTE that extracted wav files will start at 0.wav. Example: 2dxplay -e 1,4-8,10 infile.2dx')
parser.add_argument('-o', '--output-dir', default='output', help='Directory to extract files to. Will be created if not exists. Default is ./output/')

if len(sys.argv) <= 1:
    print(f"2dxPlay {version}")
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

mixer.init()

infile = args.infile
outdir = args.output_dir

try:
    twodx_file = Twodx(path.abspath(infile))
except struct.error:
    traceback.print_exc()
    print("Probably not a 2dx file.")
    sys.exit(1)
except:
    traceback.print_exc()
    sys.exit(1)

current_track = 1

# function from bemaniutils/afputils.
def parse_intlist(data):
    ints = []

    for chunk in data.split(","):
        chunk = chunk.strip()
        if '-' in chunk:
            start, end = chunk.split('-', 1)
            start_int = int(start.strip())
            end_int = int(end.strip())
            ints.extend(range(start_int, end_int + 1))
        else:
            ints.append(int(chunk))

    return sorted(set(ints))

def extract(data=None):
    if outdir != '.' and not os.path.exists(outdir):
        os.mkdir(outdir)
    if args.extract == 'all':
        for i in range(twodx_file.file_count):
            wav = twodx_file.load(i)
            print(f"Writing {i+1}/{twodx_file.file_count} wavs to {outdir}")
            with open(f"{outdir}/{i}.wav", 'wb') as f:
                f.write(wav.getbuffer())

    else:
        if data:
            ints = parse_intlist(data)
        else:
            ints = parse_intlist(args.extract)
        for i in ints:
            wav = twodx_file.load(i-1)
            print(f"Writing {i-1}.wav to {outdir}")
            with open(f"{args.output_dir}/{i-1}.wav", 'wb') as f:
                f.write(wav.getbuffer())

def main():
    if args.extract:
        extract()
        sys.exit()

    global current_track
    try:
        while current_track-1 < twodx_file.file_count:
            wav = twodx_file.load(current_track-1)
            sound = mixer.Sound(wav)
            channel = sound.play()
            length = timedelta(seconds=int(sound.get_length()))
            print(f"Playing: {infile}    Track {current_track}/{twodx_file.file_count}    Length: {length}")
            while channel.get_busy():
                pass
            current_track += 1
    except KeyboardInterrupt:
        mixer.stop()
        while "the answer is invalid":
            try:
                reply = str(input('Enter track number to jump to, e [track(s) to extract], or q to quit: ')).lower().strip()
            except (EOFError, KeyboardInterrupt):
                sys.exit(0)

            if reply == 'q':
                sys.exit(0)
            if reply[0] == 'e':
                ints = reply.split()
                if len(reply) > 1:
                    extract(reply.split()[1])
                else:
                    continue
            if reply.isdigit() and int(reply) in range(1, twodx_file.file_count + 1):
                current_track = int(reply)
                main()

    except Exception:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

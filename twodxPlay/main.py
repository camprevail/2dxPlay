import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from os import path
from pygame import mixer
from twodxPlay.twodx import Twodx
import sys, traceback
from datetime import timedelta
import struct


if len(sys.argv) <= 1:
    print("2dxPlay V1.0.0")
    print("Usage: 2dxplay infile.2dx")
    sys.exit(1)

infile = sys.argv[1]

mixer.init()

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

def main():
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
                reply = str(input('Enter track number to jump to, or q to quit: ')).lower().strip()
            except (EOFError, KeyboardInterrupt):
                sys.exit(0)

            if reply == 'q':
                sys.exit(0)
            if reply.isdigit() and int(reply) in range(1, twodx_file.file_count + 1):
                current_track = int(reply)
                main()

    except Exception:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

import struct
from io import BytesIO


# 2dx file structure ported from https://github.com/mon/2dxTools
class Twodx:

    def __init__(self, path):
        self.path = path
        try:
            with open(self.path, 'rb') as f:
                self.name = f.read(16)
                self.header_size = struct.unpack('I', f.read(4))[0]
                self.file_count = struct.unpack('I', f.read(4))[0]
                f.seek(48, 1)
                self.file_offsets = [struct.unpack('I', f.read(4))[0] for i in range(self.file_count)]
        except:
            raise

    def load(self, file: int):
        with open(self.path, 'rb') as f:
            f.seek(self.file_offsets[file])
            dx = f.read(4)
            header_size = struct.unpack('I', f.read(4))[0]  # Should be "2DX9";
            wav_size = struct.unpack('I', f.read(4))[0]  # Always 24 bytes, includes dx chars
            unk1 = struct.unpack('h', f.read(2))[0]  # Always 0x3231
            track_id = struct.unpack('h', f.read(2))[0]  # Always -1 for previews, 0-7 for song + effected versions, 9 to 11 used for a few effects
            unk2 = struct.unpack('h', f.read(2))[0]  # All 64, except song selection change 'click' is 40
            attenuation = struct.unpack('h', f.read(2))[0]  #  0-127 for varying quietness
            loop_point = struct.unpack('I', f.read(4))[0]  #  Sample to loop at * 4

            f.seek(self.file_offsets[file] + header_size)
            wav = BytesIO(f.read(wav_size))
            return wav

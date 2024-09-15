import os, sys

files = {}


def unpack(byt: bytes | bytearray):
    global fs
    files = {}
    meta = byt[0:256]
    mt = b""
    for i in range(32):
        file_meta = byt[i * 8: (i + 1) * 8]
        name = file_meta[0:4]
        if (name) == b"$inf":
            start_pos = file_meta[4] << 8 | file_meta[5]
            end_pos = file_meta[6] << 8 | file_meta[7]
            mt = fs[start_pos:end_pos]
    for i in range(32):
        file_meta = byt[i * 8: (i + 1) * 8]
        name = file_meta[0:4]
        if not (name) in [b"$inf", b"\0\0\0\0"]:
            start_pos = file_meta[4] << 8 | file_meta[5]
            end_pos = file_meta[6] << 8 | file_meta[7]
            content = fs[start_pos:end_pos]
        
            oi = mt[i] % 2
            if oi == 0:
                ftype = "file"
            elif oi == 1:
                ftype = "folder"
            if ftype == "file":
                files[(name).decode()] = content
            elif ftype == "folder":
                files[(name).decode()] = unpack(content)
    return files

def present_files(f, path = "./"):
    for i in f:
        if type(f[i]) == dict:
            os.mkdir(path + "/" + i)
            present_files(f[i], path + "/" + i + "/")
        else:
            open(path + "/" + i, "wb").write(f[i])

file = "driver"
output = "./out/"
try:
    file = sys.argv[1]
    output = sys.argv[2]
except:
    pass
try:
    a = open(file, "rb").read()

    fs = a
    present_files(unpack(a), path = output)
except:
    print("An unexpected error happened while reading make sure the paths are correct.")

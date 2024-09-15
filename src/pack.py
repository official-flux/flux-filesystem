import os, time, sys

files = {}
biggest = 0

def bc(i: int):
    global biggest
    if i > biggest:
        biggest = i
class con:
    driver = bytearray(b"\0" * 65536)
def convert(files, intor = 0, where = 256, k = 0):
    p = -1
    km = b""
    for i in files:
        p += 1
        if type(files[i]) == bytes:
            con.driver[intor:intor + 4] = i[0:4]
            con.driver[intor + 4:intor + 6] = where.to_bytes(2)
            con.driver[intor + 6:intor + 8] = (len(files[i]) + where).to_bytes(2)
            con.driver[where:where + len(files[i])] = files[i]
            where += len(files[i])
            
            intor += 8
            km += b"\0"
        elif type(files[i]) == dict:
            con.driver[intor:intor + 4] = i[0:4]
            con.driver[intor + 4:intor + 6] = where.to_bytes(2)
            con.driver[intor + 6:intor + 8] = (256 + where).to_bytes(2)
            h = convert(files[i], intor = where, where = where + 256)
            where = h[0]
            intor += 8
            km += b"\1"
        else:
            print(f"files should be byte or dict got {str(type(files[i])).upper()} instead.")
    km = km + (b"\0" * (32 - len(km)))
    con.driver[intor:intor + 4] = b"$inf"
    con.driver[intor + 4:intor + 6] = where.to_bytes(2)
    con.driver[intor + 6:intor + 8] = (len(km) + where).to_bytes(2)
    con.driver[where:where + len(km)] = km
    where += len(km)
    intor += 8
    bc(intor)
    bc(where)
    return (where, intor)
def map_directory(path = './out'):
    file_structure = {}
    for entry in os.listdir(path):
        try:
            full_path = os.path.join(path, entry)
            if os.path.isfile(full_path):
                print("[PACKING] <FILE> " + full_path)
                with open(full_path, 'rb') as file:
                    file_structure[bytes(entry, 'utf-8')[0:4]] = file.read()
            elif os.path.isdir(full_path):
                print("[PACKING] <FOLDER> " + full_path)
                file_structure[bytes(entry, 'utf-8')[0:4]] = map_directory(full_path)
        except:
            pass
    return file_structure
class void:
    __slots__ = ()
try:
    qut = 0
    p = -1
    args = sys.argv[1:]
    output = "driver"
    pth = "./"
    var = False
    while (p < len(args)-1):
        p += 1
        arg = args[p]
        if arg.startswith("--"):
            name = arg[2:]
            if name == "vsize":
                var = True

        elif arg.startswith("-"):
            name = arg[1:]
            if name in ["o", "output"]:
                try:
                    p += 1
                    output = args[p]
                except:
                    pass
        else:
            pth = arg
    files = map_directory(pth)
    try:
        convert(files, k = 1)
    except:
        print("[ERROR] FOLDER TOO BIG TO CONVERT 64 KILOBYTES MAXIMUM.")
        qut = 1
        sys.exit()
    
    if var:
        con.driver = con.driver[0:biggest]
    open(output, "wb").write(con.driver)
    print("[PACKING] <FINISH> " + output)
except:
    if qut == 1:
        sys.exit()
    print("[ERROR] FOLDER DOESN'T EXIST OR IT IS A FILE.")

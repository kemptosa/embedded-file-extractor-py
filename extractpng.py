READ_CHUNK_SIZE = 2**10*8

import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
#import PIL

filename = ''

try:
    filename = sys.argv[1]
except:
    filename = dir_path + input("Enter file location: ")

def extract_png_data(file, offset):
    # directly extracts file by image chunks
    file.seek(offset)
    data = b""
    data += file.read(8) # file sig
    chunk_type = b""
    chunk_num = 0
    while chunk_type != b"IEND":
        chunk_size = file.read(4)
        chunk_type = file.read(4)
        chunk_data = file.read(int.from_bytes(chunk_size))
        chunk_cyrc = file.read(4)
        if chunk_num == 0 and chunk_type != b'IHDR': return None # if the first chunk is not a header chunk, something probably went wrong
        data += chunk_size + chunk_type + chunk_data + chunk_cyrc
        chunk_num += 1
    
    print(f"start: {hex(offset)}, len: {hex(len(data))}")
    return data

def extract_jfif_data(file, offset):
    # the jfif format is currently incomprehensible for me, so just naively search for the ending marker
    file.seek(offset)
    data = b""

    end_found = False
    last_chunk = b""
    end_offset = offset
    while not end_found:
        cur_chunk = file.read(READ_CHUNK_SIZE)
        found_local_offset = (last_chunk + cur_chunk).find(b"\xFF\xD9")
        if found_local_offset != -1:
            end_offset += found_local_offset - len(last_chunk)
            end_found = True
        else:
            end_offset += READ_CHUNK_SIZE
            last_chunk = cur_chunk
    
    file_len = (end_offset - offset) + 2
    file.seek(offset)
    print(f"start: {hex(offset)}, len: {hex(file_len)}")
    return file.read(file_len)


formats = {
    'PNG': {
        'type': 'PNG',
        'MAGIC': b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A",
        'extract': extract_png_data
    },
    'JFIF': {
        'type': 'JFIF',
        'MAGIC': b"\xFF\xD8\xFF\xE0",
        'extract': extract_jfif_data
    }
}


def find_file_offsets(file, sig):
    found = []
    offset = 0
    last_chunk = b""
    while chunk := file.read(READ_CHUNK_SIZE):
        lowest_offset = READ_CHUNK_SIZE * 3
        found_format = ''
        for format in formats:
            found_local_offset = (last_chunk + chunk).find(formats[format]['MAGIC'])
            if found_local_offset == -1: continue
            if found_local_offset < lowest_offset:
                lowest_offset = found_local_offset
                found_format = format

        if found_format != '':
            found_global_offset = offset + lowest_offset - len(last_chunk)
            found.append({'type': found_format, 'int': found_global_offset, 'str': hex(found_global_offset)})
            offset = found_global_offset + 8
            file.seek(offset)
            last_chunk = b""
        else:
            last_chunk = chunk
            offset += READ_CHUNK_SIZE
    return found



try:
    with open(filename, 'rb') as f:
        offsets = find_file_offsets(f, formats['PNG']['MAGIC'])
        print(f"found {len(offsets)} results")
        for found in offsets:
            filedata = formats[found['type']]['extract'](f, found['int'])
            length = filedata == None and '0kb' or f"{round(len(filedata)/100)/10}kb"
            print(f"{found['type']}: {found['str']}, {length} {filedata == None and '[invalid]' or ''}")
            if filedata == None: continue
            with open(f"{dir_path}/{found['str']}.{str.lower(found['type'])}", 'wb') as w:
                
                w.write(filedata)
except BaseException as e:
    print(e)


input("Press Enter to exit program")
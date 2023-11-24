import sys
import shutil
from pathlib import Path
import re

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()

def normalize(name: str) -> str: # type hint: good code maner
    t_name = name.translate(TRANS)
    t_name = re.sub(r'\W', '_', t_name)

    return t_name

# Create folders
def create_folder(object):

    if object.is_file():
        file_name, file_ext = object.stem, object.suffix 
        file_ext = file_ext.lower()
        
        # Make name normalization
        file_name_new = normalize(file_name)
        normalize_name = file_name_new + file_ext
        
        images = ('.jpeg', '.png', '.jpg', '.svg')
        video = ('.avi', '.mp4', '.mov', '.mkv')
        documents = ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')
        audio = ('.mp3', '.ogg', '.wav', '.amr')
        archives = ('.zip', '.gz', '.tar', '.rar')
        
        if file_ext in images:
            Path.mkdir(object.parent / 'images', exist_ok=True)
            object.rename(object.parent / 'images' / normalize_name)
        elif file_ext in documents:
            Path.mkdir(object.parent / 'documents', exist_ok=True)
            object.rename(object.parent / 'documents' / normalize_name) 
        elif file_ext in audio:
            Path.mkdir(object.parent / 'audio', exist_ok=True)
            object.rename(object.parent / 'audio' / normalize_name)    
        elif file_ext in video:
            Path.mkdir(object.parent / 'video', exist_ok=True)
            object.rename(object.parent / 'video' / normalize_name)  

        # Work with archives 
        elif file_ext in archives:

            try:
                Path.mkdir(object.parent / 'archives', exist_ok=True)
                object.rename(object.parent / 'archives' / normalize_name)
                shutil.unpack_archive(Path(object.parent / 'archives' / normalize_name), Path(object.parent / 'archives' / file_name))

            except shutil.ReadError:
                print("It`s not archive")
            
# The sorting process
def sorting(path):

    ignore_list = ('archives', 'video', 'audio', 'documents', 'images')

    for item in path.iterdir():

        if item.is_dir() and item.name not in ignore_list:
            sorting(item) # recursion

            # If folder if empty - delete
            if item.is_dir() and not any(item.iterdir()):
                item.rmdir()

        elif item.is_file():
            print(f'file {item}')
            print(item.parent)
            create_folder(item)
            
            
def main():
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        sorting(path)
    else:
        print("Enter folder")

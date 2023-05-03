import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", required=True, type=str, help="The image file you want to load your message into.")
parser.add_argument("-r", "--read",required=False, action="store_true", help="Prints out the message from the image.")
parser.add_argument("-w", "--write", required=False, action="store_true")
parser.add_argument("-c", "--clear", required=False, action="store_true", help="Purges the content of the image")
parser.add_argument("-o", "--overwrite", required=False, action="store_true", help="Additional parameter for writing.")
parser.add_argument("-l", "--load", required=False, type=str, help="Loads the content of the file into the image")

def write_to_image(path: str, content: str) -> None: 
    with open(path, "ab") as file: 
        file.write(content.encode())

def read_from_image( path: str ) -> str:
    with open(path, "rb") as file:
        img = bytearray( file.read() )
        EOI = img.index(b"\xff\xd9") + 2
        message = img[EOI:]
    return message.decode()

def clear_from_image( path: str ) -> None: 
    with open(path, "rb") as file: 
        content = bytearray(file.read())
        content_without_message = content[ : content.index(b"\xff\xd9") + 2 ]
    with open(path, "wb") as filtered_file:
        filtered_file.write(content_without_message)
    
def load_file_into_image(image_file_path: str, loadable_file: str) -> None:
    with open(loadable_file, "r") as temp_file:
        content = temp_file.read()
    with open(image_file_path, "wb") as image_file:
        image_file.write(content.encode())


def main( args ) -> None: 
    file_path = args.file
    if not os.path.exists(  args.file ):
        raise FileNotFoundError("[*] The given image doesn't exists")
    
    if args.read: 
        print(read_from_image(file_path))
    elif args.write:
        if args.overwrite:
            clear_from_image(file_path)
        
        content = input("<<Type Here The Content You Want To Hide>> ")
        write_to_image(file_path, content)
    elif args.clear:
        clear_from_image(file_path)
    elif args.load:
        if not os.path.exist(args.load): 
            raise FileNotFoundError("[!] File wasnt found")
        load_file_into_image(file_path, args.load)
    else:
        print("help: use -c, -w or -r")


if __name__ == "__main__":
    main(parser.parse_args())
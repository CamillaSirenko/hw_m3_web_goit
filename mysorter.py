import argparse
from pathlib import Path
from shutil import copyfile
import concurrent.futures
import logging

def grabs_folder(path: Path) -> None:
    folders = []
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            folders.extend(grabs_folder(el))
    return folders

def get_extension_category(extension):
    video_extensions = {"mp4", "mkv", "avi"}
    audio_extensions = {"mp3", "wav", "flac"}
    document_extensions = {"pdf", "docx", "txt"}
    code_extensions = {"py", "js", "html"}
    picture_extensions={"png", "jpeg", "jpg"}
    archieve_extensions={"zip", "rar"}

    if extension in video_extensions:
        return "video"
    elif extension in audio_extensions:
        return "audio"
    elif extension in document_extensions:
        return "document"
    elif extension in code_extensions:
        return "code"
    elif extension in picture_extensions:
        return "picture"
    elif extension in archieve_extensions:
        return "archieve"
    else:
        return "other"

def copy_file(path: Path, output: Path) -> None:
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]
            ext_folder = output / get_extension_category(ext)
            try:
                ext_folder.mkdir(exist_ok=True, parents=True)
                copyfile(el, ext_folder / el.name)
            except OSError as err:
                logging.error(err)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sorting folder")
    parser.add_argument("--source", "-s", help="Source folder", required=True)
    parser.add_argument("--output", "-o", help="Output folder", default="dist")
    parser.add_argument("--verbose", "-v", help="Enable verbose logging", action="store_true")
    args = parser.parse_args()

    source = Path(args.source)
    output = Path(args.output)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

    folders = [source]
    folders.extend(grabs_folder(source))
    logging.info(f"Folders to process: {folders}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for folder in folders:
            executor.submit(copy_file, folder, output)

    logging.info(f"Processing completed. You can delete {source}")

import asyncio
import argparse
import aiofiles
import shutil
import os
import logging
from pathlib import Path

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(file_path: Path, destination_folder: Path):
    """Copies a file to a folder based on its extension."""
    ext_folder = destination_folder / file_path.suffix[1:].lower()  # create a subfolder based on file extension
    ext_folder.mkdir(parents=True, exist_ok=True)  # create the subfolder if it doesn't exist

    dest_file_path = ext_folder / file_path.name

    try:
        async with aiofiles.open(file_path, 'rb') as src, aiofiles.open(dest_file_path, 'wb') as dst:
            await dst.write(await src.read())  # asynchronously copy the file
        logging.info(f'Copied file: {file_path} to {dest_file_path}')
    except Exception as e:
        logging.error(f'Error copying file {file_path} to {dest_file_path}: {e}')

async def read_folder(source_folder: Path, destination_folder: Path):
    """Recursively reads files from the source folder and copies them asynchronously."""
    tasks = []

    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = Path(root) / file
            tasks.append(copy_file(file_path, destination_folder))  # add a copy task for each file

    await asyncio.gather(*tasks)  # execute all tasks concurrently

def parse_args():
    """Argument parser for command-line arguments."""
    parser = argparse.ArgumentParser(description="Asynchronous file sorting by extension")
    parser.add_argument("source_folder", type=str, help="Path to the source folder")
    parser.add_argument("destination_folder", type=str, help="Path to the destination folder")
    return parser.parse_args()

async def main():
    args = parse_args()
    source_folder = Path(args.source_folder)
    destination_folder = Path(args.destination_folder)

    if not source_folder.exists() or not source_folder.is_dir():
        logging.error("Source folder not found or is not a directory.")
        return

    destination_folder.mkdir(parents=True, exist_ok=True)  # create the destination folder if it doesn't exist

    await read_folder(source_folder, destination_folder)

if __name__ == "__main__":
    asyncio.run(main())

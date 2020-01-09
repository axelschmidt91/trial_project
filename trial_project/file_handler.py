import os
from tkinter import *
from tkinter import filedialog
import logging


logger = logging.getLogger(__name__)


def scan_folder(folder, postfix):
    """scans folder for files ended with the specified postfix
    
    :param folder: path to choosen folder
    :type folder: str
    :param postfix: postfix of files of filetypes e.g. ".txt" or "_data.csv"
    :type postfix: str
    :return: list of str of founded file directorys
    :rtype: list
    """    
    file_dir = list()
    folder_dir = list()

    for dirpath, dirnames, filenames in os.walk(folder):
        logger.debug([dirpath, dirnames, filenames])

        for filename in [f for f in filenames if f.endswith(postfix)]:
            file = os.path.join(dirpath, filename)
            file_dir.append(file)
        for foldername in [f for f in dirnames if f.endswith(postfix)]:
            folder = os.path.join(dirpath, foldername)
            folder_dir.append(folder)

    return file_dir, folder_dir


def open_folder_dialog():
    """opens dialog to choose folder to work

    Returns:
        str -- path to folder that was choosen
    """
    root = Tk()
    root.withdraw()
    root.folder = filedialog.askdirectory()
    return root.folder

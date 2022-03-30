"""Main module used to gather all informations and launch the submodules"""
import logging
import importlib.resources
from pathlib import WindowsPath
import os
from bin.utils import get_recipients, get_pdfs
from bin.modules import watermark_pdfs

 
def get_folder_path(folder_name: str) -> WindowsPath:
    """Get directory path of the package from its name

    Args:
        folder_name (str): Name of the directory

    Raises:
        e: If the directory doesn't exist, raise a NameError

    Returns:
        WindowsPath: Path to the directory
    """
    try:
        with importlib.resources.path(folder_name, "") as p:
            folder_path = p
    except NameError as e:
        logger.error(f"Le dossier {folder_name} n'existe pas.", exc_info=True)
        raise e
    return folder_path


if __name__ == "__main__":
    #: Path to the config directory
    config_path = get_folder_path('config')
    #: Path to the data directory
    data_path = get_folder_path('data')
    #: Path to the log directory
    log_path = get_folder_path('log')
    logger = logging
    logger.basicConfig(filename=os.path.join(log_path, "app.log"), format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)
    recipients = get_recipients(config_path)
    pdfs = get_pdfs(data_path)
    watermark_pdfs(data_path, pdfs, recipients)
    logger.info("Programme terminé.")

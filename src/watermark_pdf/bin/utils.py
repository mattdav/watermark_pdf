"""Utilities needed to collect configuration"""
from pathlib import WindowsPath
import pandas as pd
import logging
import os
logger = logging.getLogger(__name__)


def get_recipients(file_path: WindowsPath) -> list:
    """Get list of recipients defined in the Excel config file

    Args:
        file_path (WindowsPath): Path to the config file

    Raises:
        e: If the file doesn't exist, raise a FileNotFoundError
        e: If "Destinataires" worksheet doesn't exist, raise a ValueError
        e: If 'Liste destinataires' column doesn't exist, raise a KeyError

    Returns:
        list: List of the recipients defined in the config file
    """
    try:
        df_recipients = pd.read_excel(open(os.path.join(file_path, 'choix_destinataires.xlsx'), 'rb'), sheet_name='Destinataires')
    except FileNotFoundError as e:
        logger.error("Le fichier 'choix_destinataires.xlsx' n'existe pas dans le dossier de configuration.", exc_info=True)
        raise e    
    except ValueError as e:
        logger.error("L'onglet 'Destinataires' n'existe pas dans le fichier de configuaration.")
        raise e
    try:
        recipients = df_recipients['Liste destinataires'].tolist()
        nb_recipients = len(recipients)
        logger.info(f"{nb_recipients} destinataires demandés dans le fichier de configuration.")
    except KeyError as e:
        logger.error("La colonne 'Liste destinataires' n'existe pas dans l'onglet 'Destinataires' du fichier de configuration.", exc_info=True)
        raise e
    return recipients


# Get list of pdfs to watermark from the data/pdf directory
def get_pdfs(data_path: WindowsPath) -> list:
    """Get the list of pdfs stored into the pdf subdirectory from the data directory

    Args:
        data_path (WindowsPath): Path of the data directory

    Raises:
        e: If the pdf subdirectory doesn't exist, raise a NameError

    Returns:
        list: List of the paths to the pdfs stored in the pdf subdirectory
    """
    pdf_path = os.path.join(data_path, 'pdf')
    try:
        pdfs = [os.path.join(pdf_path, f) for f in os.listdir(pdf_path) if f.endswith('.pdf')]
        nb_pdf = len(pdfs)
        logger.info(f"{nb_pdf} fichier à filigraner.")
    except NameError as e:
        logger.error("Le dossier 'pdf' n'existe pas dans le dossier 'data'.")
        raise e
    return pdfs

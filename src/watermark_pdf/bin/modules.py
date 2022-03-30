"""Core module developed to watermark the pdf files"""
from distutils.text_file import TextFile
from pathlib import WindowsPath
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from PyPDF4 import PdfFileWriter, PdfFileReader
import logging
import os
from io import BytesIO
from pathlib import Path  
import shutil
logger = logging.getLogger(__name__)


def create_watermarks(path: WindowsPath, recipient: str) -> list:
    """Create watermarks of both formats (portrait and landscape) for the defined recipient and save them to a temp directory

    Args:
        path (WindowsPath): Path to the temp directory
        recipient (str): Name of the recipient to put in the watermark

    Returns:
        list: List of the paths to the watermarks
    """
    p_path = os.path.join(path, f"watermark_portrait_{recipient}.pdf")
    ls_path = os.path.join(path, f"watermark_landscape_{recipient}.pdf")
    p = canvas.Canvas(p_path)
    p.saveState()
    p.setFillColor(HexColor('#dee0ea'))
    p.setFont("Helvetica", 20)
    p.translate(10.5*cm, 14.85*cm)
    p.rotate(45)
    for i in range(0, 3):
        for j in range(0, 3):
            p.drawCentredString(j*10*cm, i*7*cm, recipient)
            p.drawCentredString(-j*10*cm, i*7*cm, recipient)
            p.drawCentredString(j*10*cm, -i*7*cm, recipient)
            p.drawCentredString(-j*10*cm, -i*7*cm, recipient)
    p.restoreState()
    p.showPage()
    p.save()
    ls = canvas.Canvas(ls_path, pagesize=(landscape(A4)))
    ls.saveState()
    ls.setFillColor(HexColor('#dee0ea'))
    ls.setFont("Helvetica", 20)
    ls.translate(14.85*cm, 10.5*cm)
    ls.rotate(45)
    for i in range(0, 3):
        for j in range(0, 5):
            ls.drawCentredString(j*10*cm, i*7*cm, recipient)
            ls.drawCentredString(j*10*cm, -i*7*cm, recipient)
            ls.drawCentredString(-j*10*cm, i*7*cm, recipient)
            ls.drawCentredString(-j*10*cm, -i*7*cm, recipient)
    ls.restoreState()
    ls.showPage()
    ls.save()
    return [p_path, ls_path]


def watermark_pdf(file: WindowsPath, watermark_list: list) -> TextFile:
    """Watermark a pdf according to the page's formats

    Args:
        file (WindowsPath): Path to the pdf
        watermark_list (list): List of the paths to the two watermarks previously created

    Returns:
        TextFile: Pdf watermarked
    """
    output_file = PdfFileWriter()
    with open(file, "rb") as f:
        input_file = PdfFileReader(f)
        page_count = input_file.getNumPages()
        for page_number in range(page_count):
            input_page = input_file.getPage(page_number)
            tmp = BytesIO()
            pageDim = input_file.getPage(page_number).mediaBox
            if (pageDim.getUpperRight_x() - pageDim.getUpperLeft_x()) > \
                    (pageDim.getUpperRight_y() - pageDim.getLowerRight_y()):
                with open(watermark_list[1], "rb") as g:
                    watermark = PdfFileReader(g)
                    new_page = watermark.getPage(0)
                    new_page.mergePage(input_page)
                    new_page.compressContentStreams()
                    output_file.addPage(new_page)
                    output_file.write(tmp)
                    if page_number == page_count - 1:
                        pdf = tmp
            else:
                with open(watermark_list[0], "rb") as h:
                    watermark = PdfFileReader(h)
                    new_page = watermark.getPage(0)
                    new_page.mergePage(input_page)
                    new_page.compressContentStreams()
                    output_file.addPage(new_page)
                    output_file.write(tmp)
                    if page_number == page_count - 1:
                        pdf = tmp
    return pdf


def printFile(path: WindowsPath, filename: str, output: TextFile, recipient):
    """Save the processed pdf to the resulting directory

    Args:
        path (WindowsPath): Path to the data directory
        filename (str): Name of the pdf watermarked
        output (TextFile): Pdf watermarked
        recipient (_type_): Name of the recipient watermarked on the pdf
    """
    folder_path = os.path.join(path, 'avec_filigrane')
    output_path = os.path.join(folder_path, f"{filename}_{recipient}.pdf")
    with open(output_path, "wb") as outputStream:
        outputStream.write(output.getvalue())


def watermark_pdfs(path: WindowsPath, pdfs: list, recipients: list):
    """Process all pdfs in the list with each name defined in the config file

    Args:
        path (WindowsPath): Path to the data directory
        pdfs (list): List of the pdfs to process
        recipients (list): List of the recipients to watermark on the different pdfs
    """
    temp_path = os.path.join(path, 'temp')
    try:
        os.mkdir(temp_path)
    except FileExistsError as e:
        pass
    watermarks = {recipient:create_watermarks(temp_path, recipient) for recipient in recipients}
    for pdf in pdfs:
        filename = Path(pdf).stem
        for key, value in watermarks.items():
            output = watermark_pdf(pdf, value)
            printFile(path, filename, output, key)
            logger.info(f"Fichier {filename} filigrané pour le destinataire {key}")
    shutil.rmtree(temp_path) 

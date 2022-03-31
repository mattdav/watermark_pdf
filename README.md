# watermark_pdf

Python package to watermark pdf files from a list of names.

## Installation

Get the package from Github

```bash
git clone https://github.com/mattdav/watermark_pdf.git
```

## Usage

1) Make sure to install all dependencies listed from the requirements
```bash
pip install -r /path/to/requirements.txt
```
1) Create your own recipients list from the template "choix_destinataires_mock.xlsx" located in the "src\watermark_pdf\config" subdirectory.
2) Rename the mock file from "choix_destinataires_mock.xlsx" to "choix_destinataires.xlsx"
3) Store your PDFs to process to the "src\watermark_pdf\data\pdf" subdirectory.
4) Launch the module
```bash
python -m path/to/package/directory/src/watermark_pdf
```
5) Collect your processed PDFs from the "src\watermark_pdf\data\avec_filigrane" subdirectory

PS : In case of trouble, check what cause problem from the app.log file located in the "src\watermark_pdf\log" subdirectory.

## Support 
If you have any questions or need any help using this program, you can email me at: matthieu.daviaud@gmail.com

## Contributing
Pull requests are welcome.

## Todo

Implement tests.
Package module for pip installation.

## License
[MIT](https://choosealicense.com/licenses/mit/)
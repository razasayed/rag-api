from PyPDF2 import PdfReader, PdfWriter

def extract_pages(input_pdf, output_pdf, pages_to_extract):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page_num in pages_to_extract:
        writer.add_page(reader.pages[page_num - 1])

    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)

input_pdf = 'soc.pdf'
output_pdf = 'small_soc.pdf'
pages_to_extract = [18,19]  # List of page numbers to extract

extract_pages(input_pdf, output_pdf, pages_to_extract)

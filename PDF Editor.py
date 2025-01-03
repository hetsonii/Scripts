import os
import fitz  # PyMuPDF

def replace_text_in_pdf(pdf_path, old_text, new_text, folder_name):
    output_folder = os.path.join(os.getcwd(), folder_name)
    os.makedirs(output_folder, exist_ok=True)

    pdf_document = fitz.open(pdf_path)

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text_instances = page.search_for(old_text)

        for inst in text_instances:
            # Redact (remove) the old text by drawing a filled rectangle over it
            page.add_redact_annot(inst)
            page.apply_redactions()

            # Get the coordinates of the old text bounding box
            x0, y0, x1, y1 = inst
            rect_width = x1 - x0
            rect_height = y1 - y0

            # Set a font size (you can adjust this)
            font_size = rect_height * 0.8  # Adjust to fit the bounding box

            # Load the default font
            font = fitz.Font()  # Default font, or you can load a custom font

            # Calculate the width of the new text based on the font size
            new_text_width = font.text_length(new_text, fontsize=font_size)

            # Calculate the position for the new text so it is centered horizontally and vertically
            new_text_x = x0 + (rect_width - new_text_width) / 2
            new_text_y = y0 + (rect_height + font_size) / 2

            # Insert the new text at the calculated position
            page.insert_text((new_text_x, new_text_y), new_text, fontsize=font_size)

    new_pdf_path = os.path.join(output_folder, os.path.basename(pdf_path).replace(old_text, new_text))
    pdf_document.save(new_pdf_path)
    pdf_document.close()

if _name_ == "_main_":
    directory = os.getcwd()  
    files = os.listdir(directory)

    old_text = 'text to replace'  # Text to search for
    new_text = 'text to replace with'  # Text to replace
    filename = 'filename to search'  # Filename to search for in the directory
    folder_name = filename + "_modified"  # Folder name for storing modified PDFs

    # Iterate through files in the current directory
    for file in files:
        if file.startswith(filename) and file.endswith('.pdf'):
            pdf_path = os.path.join(directory, file)
            replace_text_in_pdf(pdf_path, old_text, new_text, folder_name)

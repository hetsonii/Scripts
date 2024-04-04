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
            text = page.get_text("text", clip=inst)
            
            # Check if the text starts with old_text
            if text.startswith(old_text):
                # Get the rectangle coordinates
                x0, y0, x1, y1 = inst
                # Calculate the vertical position for the new text
                font_size = inst[3] - inst[1]
                new_text_y = y0 + font_size
                # Remove the old text by drawing a filled rectangle
                page.draw_rect(fitz.Rect(x0, y0, x1, y1), fill=(1, 1, 1), width=0)
                # Insert the new text at the calculated position
                page.insert_text((x0, new_text_y), new_text)


    new_pdf_path = os.path.join(output_folder, os.path.basename(pdf_path).replace(old_text, new_text))
    pdf_document.save(new_pdf_path)
    pdf_document.close()

if __name__ == "__main__":
    directory = os.getcwd()  
    files = os.listdir(directory)

    old_text = 'text_to_be_replaced'
    new_text = 'my_new_text'
    filename = 'files_to_be_scanned'
    folder_name = filename + "_modified"  # Folder name for storing modified PDFs

    # Iterate through files in the current directory
    for file in files:
        if file.startswith(filename) and file.endswith('.pdf'):
            pdf_path = os.path.join(directory, file)
            replace_text_in_pdf(pdf_path, old_text, new_text, folder_name)
            

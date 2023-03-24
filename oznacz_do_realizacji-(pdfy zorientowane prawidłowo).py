#bmystek
import os
import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import shutil
import os
import pymsgbox

 
# ***************tworzenie kopii struktury katalogów *******************

# defining the function to ignore the files
# if present in any folder
def ignore_files(dir, files):
    return [f for f in files if os.path.isfile(os.path.join(dir, f))]
 
# calling the shutil.copytree() method and
# passing the src,dst,and ignore parameter

input_dir = os.getcwd()
output_dir = '{}\\{}'.format(input_dir,'_do realizacji')

if not os.path.exists(output_dir):
    shutil.copytree(input_dir,
                    output_dir,
                    ignore=ignore_files)

# ***************tworzenie kopii struktury katalogów *******************


global new_pdf


# liczniki
pdf_c=0
files_c=0
pdf_r=0

input_dir = os.getcwd()

folder_path = input_dir
output_folder = '{}\\_do realizacji'.format(input_dir)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def make_can(pdf_w,pdf_h):
    global new_pdf
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(int(pdf_w),int(pdf_h)))

    can.setFillColorRGB(255,0,0) #kolor czcionki
    can.setFont("Helvetica", 12) #font i jego wielkość
    can.drawString(pdf_w-cd_x,cd_y,"DO REALIZACJI") # tekst i jego lokalizacja
    can.save()
    packet.seek(0)
    new_pdf = PdfReader(packet)

for path,_,files in os.walk(folder_path):
    if '_do realizacji' in path:continue
    else:
        for pdf_file in files:
            files_c+=1
            if pdf_file.endswith(".pdf"):
                pdf_c+=1
                pdf_reader = PdfReader(open('{}\\{}'.format(path, pdf_file), "rb"))
                pdf_w,pdf_h=pdf_reader.pages[0].mediabox[-2:]

                # odległości do prawego dolnego narożnika
                if pdf_reader.numPages==1:
                    cd_x,cd_y=[110,21] #rysunki
                else:
                    cd_x,cd_y=[160,800] # opisy techniczne - wersja dla prawego górnego naroznika
                    # cd_x,cd_y=[160,55] # opisy techniczne - wersja dla prawego dolnego naroznika

                make_can(pdf_w,pdf_h)

                pdf_merged = pdf_reader.pages[0]
                pdf_merged.merge_page(new_pdf.pages[0])
                pdf_writer = PdfWriter()
                
                for i in range(len(pdf_reader.pages)):
                    if i == 0:
                        pdf_writer.add_page(pdf_merged)
                    else:
                        pdf_writer.add_page(pdf_reader.pages[i])

                # ściażka dostępu do nowej lokalizacji pliku
                n_file='{}\\{}'.format(path, pdf_file)[len(folder_path):]
                n_file='{}\\_do realizacji\\{}'.format(folder_path,n_file)

                with open(n_file, "wb") as output_file:
                    pdf_writer.write(output_file)

        print("Dodano oznacznia 'Do realizacji'.")

pymsgbox.alert("Oznaczenia zostały dodane.( pdfy:{}, pominięte inne pliki:{} )".format(pdf_c,files_c-pdf_c))
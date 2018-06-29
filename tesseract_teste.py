from PIL import Image # Importando o módulo Pillow para abrir a imagem no script

import pytesseract # Módulo para a utilização da tecnologia OCR

filename = str(input()).strip()
print( pytesseract.image_to_string( Image.open(filename) ) ) # Extraindo o texto da imagem

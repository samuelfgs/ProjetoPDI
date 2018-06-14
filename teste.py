from tesserocr import PyTessBaseAPI

images = ['images/img01.jpg', 'images/t1.png', 'images/t2.png', 'images/t3.png']

with PyTessBaseAPI() as api:
    for img in images:
        print (img)
        print ('###################################################')
        api.SetImageFile(img)
        print (api.GetUTF8Text())
        print (api.AllWordConfidences())
        print('\n\n\n')
        print ('###################################################')

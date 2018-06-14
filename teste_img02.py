from tesserocr import PyTessBaseAPI

images = ['images/img02.jpg']

with PyTessBaseAPI() as api:
    for img in images:
        print (img)
        print ('###################################################')
        api.SetImageFile(img)
        print (api.GetUTF8Text())
        print (api.AllWordConfidences())
        print('\n\n\n')
        print ('###################################################')

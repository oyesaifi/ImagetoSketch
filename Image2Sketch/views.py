from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
import cv2
import random
import string
import shutil
import os

class Home(TemplateView):
    template_name = 'home.html'

def home(request):
    return render(request, 'home.html')

def privacypolicy(request):
    return render(request, 'policy.html')

def sitemap(request):
    return render(request, 'sitemap.xml')

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['ImageUpload']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        pathOFimage = 'media/' + uploaded_file.name

        image = cv2.imread(pathOFimage)
        grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        invert = cv2.bitwise_not(grey_img)
        blur = cv2.GaussianBlur(invert, (21,21),0)
        invertedblur = cv2.bitwise_not(blur)
        sketch = cv2.divide(grey_img, invertedblur, scale=256.0)
        N = 7
        res = ''.join(random.choices(string.ascii_uppercase +
                                    string.digits, k = N))
        cv2.imwrite(str(res)+"_sketch.png", sketch)
        data = str(res)+"_sketch.png"
        shutil.move(data, "sketch/" + data)
        data = 'sketch/' + str(res) + "_sketch.png"
        os.remove(pathOFimage)
        return render(request, 'final.html', {'data':data})

import os
import io
import tempfile

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import serializers
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response

# from PIL import Image
import torch
import fastai
from fastai.vision import *

path = os.getcwd()
defaults.device = torch.device('cpu')
learn = load_learner(path)
# print(learn)
# print(path)
# classes= ['chanel bag', 'bulgari bag', 'coach bag', 'hermes bag', 'lv bag', 'miumiu bag', 'prada bag']
# ImageDataBunch.single_from_classes(path, classes, ds_tfms)

class PredictionSerializer(serializers.Serializer):
    prediction = serializers.CharField()

class FileUploadView(APIView):
    # code wouldn't work when I used fileuploadparser; if i use multipart/form-data, then use multipartparser
    parser_classes = (MultiPartParser, )

    def post(self, request, format=None):
        try:
            file_obj = request.FILES['file']
        except Exception as e:
            print('error')
            print(e)
            return Response(status=415)

        img = open_image(file_obj.file)
        prediction = str(learn.predict(img)[0])
        p = PredictionSerializer({'prediction': prediction})
        return Response(p.data)


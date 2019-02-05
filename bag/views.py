import datetime
import os
import io
import tempfile

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response

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

class FeedbackView(APIView):
    parser_classes = (JSONParser, )

    def post(self, request, format=None):
        print('uploading feedback')
        filename = '{}_{}'.format(datetime.date.today().strftime('%Y-%m-%d'), request.data['filename'])
        text = '{},{},{}\n'.format(filename, request.data['userFeedbackPrediction'], request.data['userGuess'])

        with open('files/list.txt', 'a') as f:
            f.write(text)
        return Response(status=204)

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

        # has a minute indicator to prevent overwriding
        filename = 'files/{}_{}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), file_obj.name)
        with open(filename, 'wb') as f:
            f.write(file_obj.read())            

        img = open_image(filename)
        prediction = str(learn.predict(img)[0])
        p = PredictionSerializer({'prediction': prediction})
        return Response(p.data)

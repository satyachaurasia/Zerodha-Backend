from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from rest_framework import status
from rest_framework.response import Response

import redis
import json

from django.http import HttpResponse
from wsgiref.util import FileWrapper

import csv

from django.http import StreamingHttpResponse


class Echo:
    def write(self, value):
        return value



r = redis.Redis(host='localhost', port=6379, db=2)

# Create your views here.

@api_view(('GET',))
@permission_classes([AllowAny,])
def get_records(request):
    '''
    Takes date and the search query 
    Returns List of records 
    '''
    q = request.GET.get('q', '')
    date = request.GET.get('date', '')
    query_list = []
    
    for key in r.scan_iter(match=f'{date} {q.upper()}*'):
        if r.get(key) is not None:
            query_list.append(json.loads(r.get(key).decode('utf-8')))
    return Response(query_list , status = status.HTTP_200_OK)



def iter_items(date, q, pseudo_buffer):
    fieldnames = ['CODE', 'NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE']
    writer = csv.DictWriter(pseudo_buffer, fieldnames=fieldnames)
    fieldnames = ['CODE', 'NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE']
    header = dict(zip(fieldnames, fieldnames))

    yield writer.writerow(header)

    for key in r.scan_iter(match=f'{date} {q.upper()}*'):
        if r.get(key) is not None:
            yield writer.writerow(json.loads(r.get(key).decode('utf-8')))



@api_view(('GET',))
@permission_classes([AllowAny,])
def download_csv(request):
    '''
    Takes date and the search query 
    Returns CSV contaning records filtered from redis DB
    '''

    q = request.GET.get('q', '')
    date = request.GET.get('date', '')

    response = StreamingHttpResponse(
        streaming_content=(iter_items(date, q, Echo())),
        content_type='text/csv',
    )

    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    return response



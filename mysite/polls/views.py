from django.shortcuts import render
from django.http import JsonResponse
import json

from .utils.answer import handle_query

def chat(request):
    return render(request, 'mysite/chat.html')

def answer(request):
    question = request.GET.get('question')
    answer = handle_query(question)
    return JsonResponse({"answer":answer})
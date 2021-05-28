from django.shortcuts import render
import psutil

def index(request):
    memory = psutil.virtual_memory()
    context = {
        'memory': memory.percent,
    }
    return render(request, 'index.html', context)

    # return render(request, 'index.html', {})
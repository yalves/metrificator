from django.shortcuts import render
from django.http import HttpResponse

import psutil

def memory(request):
  memory = psutil.virtual_memory()
  context = {
      'memory': memory.percent,
  }
  return render(request, 'memory.html', context)

def disk(request):
  memory = psutil.virtual_memory()
  disk = psutil.disk_usage('.')
  context = {
      'disk_total': round(disk.total/(1024*1024*1024), 2),
      'disk_used': round(disk.used/(1024*1024*1024), 2),
      'disk_free': round(disk.free/(1024*1024*1024), 2),
      'disk_percentage': disk.percent,
  }
  return render(request, 'disk.html', context)


def memory_percentage(request):
  memory = psutil.virtual_memory()
  return HttpResponse(memory.percent)
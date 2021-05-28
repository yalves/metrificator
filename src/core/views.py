from django.shortcuts import render
import psutil

def index(request):
  memory = psutil.virtual_memory()
  context = {
      'memory': memory.percent,
  }
  return render(request, 'index.html', context)

def disk(request):
  memory = psutil.virtual_memory()
  disk = psutil.disk_usage('.')
  context = {
      'disk_total': round(disk.total/(1024*1024*1024), 2),
      'disk_used': round(disk.used/(1024*1024*1024), 2),
      'disk_free': round(disk.free/(1024*1024*1024), 2),
  }
  return render(request, 'disk.html', context)
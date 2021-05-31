from django.shortcuts import render
from django.http import HttpResponse

import platform
import psutil

def memory(request):
  memory = psutil.virtual_memory()
  context = {
      'memory': memory.percent,
  }
  return render(request, 'memory.html', context)

def memory_percentage(request):
  memory = psutil.virtual_memory()
  return HttpResponse(memory.percent)

def disk(request):
  disk = psutil.disk_usage('.')
  context = {
      'disk_total': round(disk.total/(1024*1024*1024), 2),
      'disk_used': round(disk.used/(1024*1024*1024), 2),
      'disk_free': round(disk.free/(1024*1024*1024), 2),
      'disk_percentage': disk.percent,
  }
  return render(request, 'disk.html', context)

def network(request):
  network = psutil.net_if_addrs()
  firstKey = list(network.keys())[0]
  ip = network[firstKey][1].address
  context = {
    'ip': ip
  }
  return render(request, 'network.html', context)

def cpu(request):
  context = {
    'processor': platform.processor(),
    'node': platform.node(),
    'platform': platform.platform(),
    'system': platform.system(),
  }
  return render(request, 'cpu.html', context)

def cpu_percentage(request):
  cpu_percentage = psutil.cpu_percent()
  return HttpResponse(cpu_percentage)


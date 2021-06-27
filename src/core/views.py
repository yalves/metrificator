from django.shortcuts import render
from django.http import HttpResponse
from os import listdir
from os.path import isfile, join
from pathlib import Path


import platform
import psutil

def index(request):
  memory = psutil.virtual_memory()
  disk = psutil.disk_usage('.')
  network = psutil.net_if_addrs()
  firstKey = list(network.keys())[0]
  ip = network[firstKey][1].address
  cpu_percentage = psutil.cpu_percent()
  context = {
      'memory': memory.percent,
      'disk_total': round(disk.total/(1024*1024*1024), 2),
      'disk_used': round(disk.used/(1024*1024*1024), 2),
      'disk_free': round(disk.free/(1024*1024*1024), 2),
      'disk_percentage': disk.percent,
      'ip': ip,
      'processor': platform.processor(),
      'node': platform.node(),
      'platform': platform.platform(),
      'system': platform.system(),
      'cpu_percent': cpu_percentage,
  }
  return render(request, 'index.html', context)

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

def files(request):
  path = Path(__file__).parent.parent
  files = [f for f in listdir(path) if isfile(join(path, f))]
  directories = [f for f in listdir(path) if not isfile(join(path, f))]
  context = {
    'files': ', '.join(files),
    'directories': ', '.join(directories),
  }
  return render(request, 'files.html', context)

def processes(request):
  processes = []

  for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
        print(pinfo)
        pinfo['memory_percent'] = round(pinfo['memory_percent'], 3)
        processes.append(pinfo)
    except psutil.NoSuchProcess:
        pass
    else:
        print(pinfo)

  context = {
    'processes': processes,
  }
  return render(request, 'processes.html', context)


from django.shortcuts import render
from django.http import HttpResponse
from os import listdir
import os, re
from os.path import isfile, join
from pathlib import Path

import platform
import psutil
import time

def index(request):
  start_time = time.time()
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
  print("--- %s seconds elapsed in 'index' call ---" % (time.time() - start_time))
  return render(request, 'index.html', context)

def memory(request):
  start_time = time.time()
  memory = psutil.virtual_memory()
  context = {
      'memory': memory.percent,
  }
  print("--- %s seconds elapsed in 'memory' call ---" % (time.time() - start_time))
  return render(request, 'memory.html', context)

def memory_percentage(request):
  start_time = time.time()
  memory = psutil.virtual_memory()
  print("--- %s seconds elapsed in 'memory_percentage' call ---" % (time.time() - start_time))
  return HttpResponse(memory.percent)

def disk(request):
  start_time = time.time()
  disk = psutil.disk_usage('.')
  context = {
      'disk_total': round(disk.total/(1024*1024*1024), 2),
      'disk_used': round(disk.used/(1024*1024*1024), 2),
      'disk_free': round(disk.free/(1024*1024*1024), 2),
      'disk_percentage': disk.percent,
  }
  print("--- %s seconds elapsed in 'disk' call ---" % (time.time() - start_time))
  return render(request, 'disk.html', context)

def network(request):
  start_time = time.time()
  context = {}

  try:
    full_results = [re.findall('^[\w\?\.]+|(?<=\s)\([\d\.]+\)|(?<=at\s)[\w\:]+', i) for i in os.popen('arp -a')]
    final_results = [dict(zip(['IP', 'LAN_IP', 'MAC_ADDRESS'], i)) for i in full_results]
    final_results = [{**i, **{'LAN_IP':i['LAN_IP'][1:-1]}} for i in final_results]
    network = psutil.net_if_addrs()
    firstKey = list(network.keys())[1]
    ip = network[firstKey][1].address
    connections = psutil.net_connections()
    context = {
      'ip': ip,
      'network': final_results,
      'connections': connections
    }
  except psutil.AccessDenied:
    pass
  
  print("--- %s seconds elapsed in 'network' call ---" % (time.time() - start_time))
  return render(request, 'network.html', context)

def cpu(request):
  start_time = time.time()
  context = {
    'processor': platform.processor(),
    'node': platform.node(),
    'platform': platform.platform(),
    'system': platform.system(),
  }
  print("--- %s seconds elapsed in 'cpu' call ---" % (time.time() - start_time))
  return render(request, 'cpu.html', context)

def cpu_percentage(request):
  start_time = time.time()
  cpu_percentage = psutil.cpu_percent()
  print("--- %s seconds elapsed in 'cpu_percentage' call ---" % (time.time() - start_time))
  return HttpResponse(cpu_percentage)

def files(request):
  start_time = time.time()
  path = Path(__file__).parent.parent
  files = [f for f in listdir(path) if isfile(join(path, f))]
  directories = [f for f in listdir(path) if not isfile(join(path, f))]
  context = {
    'files': ', '.join(files),
    'directories': ', '.join(directories),
  }
  print("--- %s seconds elapsed in 'files' call ---" % (time.time() - start_time))
  return render(request, 'files.html', context)

def processes(request):
  start_time = time.time()
  processes = []

  for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])        
        pinfo['memory_percent'] = 0.0 if pinfo['memory_percent'] == None else round(pinfo['memory_percent'], 3)
        if(pinfo['memory_percent'] > 0.0 or pinfo['cpu_percent'] != None):
          processes.append(pinfo)
    except psutil.NoSuchProcess:
        pass
    except psutil.AccessDenied:
        pass

  context = {
    'processes': processes,
  }
  print("--- %s seconds elapsed in 'processes' call ---" % (time.time() - start_time))
  return render(request, 'processes.html', context)


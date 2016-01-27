import base64, json
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
import subprocess
import requests
import re
import uuid

class Index(View):
	def get(self, request):
		return HttpResponse('hi')

class List(View):
	def get(self, request):
		return HttpResponse('<pre>{}</pre>'.format(subprocess.getoutput('lxc-ls --fancy')))

class Run(View):
	def post(self, request, ip=None):
		if ip:
			ip = '10.0.'+ip
			isnew = False
		else:
			name = 'u1-'+uuid.uuid4().hex
			ephemeral = subprocess.getoutput('unset XDG_SESSION_ID XDG_RUNTIME_DIR; cgm movepid all virt $$; lxc-start-ephemeral -o u1 -n {} --storage-type tmpfs --daemon'.format(name))
			ip = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ephemeral)[0]
			isnew = True

		res = requests.post('http://'+ip, data=request.POST).json()
		res['ip'] = ip.replace('10.0.', '')
		res['isnew'] = isnew

		return JsonResponse(res)

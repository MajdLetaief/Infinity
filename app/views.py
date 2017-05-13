from django.shortcuts import render
from django.shortcuts import render

import json
import requests
# Create your views here.
def AuthView(request):
    url = "http://192.168.114.130/identity/v3/auth/tokens"
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        print(username + " ---- " + password)

        data = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": username,
                            "domain": {
                                "name": "Default"
                            },
                            "password": password
                        }
                    }
                }
            }
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        assert r.status_code == 201
        x = r.json()
        request.session['X-Token'] = r.headers.get('X-Subject-Token')
        request.session['X-Project'] = x['token']['project']['id']

        prname = x['token']['project']['name']




    return render(request, 'app/index.html', {"username":username})


def LoginView(request):

        # return render()
    return render(request, 'app/login.html', {})
def VolumeView(request):
    token =  request.session['X-Token']
    projectid = request.session['X-Project']
    url = "http://192.168.114.130:8776/v3/"+projectid+"/volumes/detail"
    l={'X-Auth-Token':token}
    r = requests.get(url,headers=l)
    x=r.json()
    vname = x['volumes']

    return render(request, 'app/volume.html', {'vname':vname})

def AddVolumeView(request):
    vname = request.POST['vname']
    vsize = request.POST['vsize']
    vdesc = request.POST['vdesc']
    token = request.session['X-Token']
    projectid = request.session['X-Project']
    url = "http://192.168.114.130:8776/v3/" + projectid + "/volumes"
    if request.POST:
        vname = request.POST['vname']
        vsize = request.POST['vsize']
        vdesc = request.POST['vdesc']
        data = {
        "volume": {
            "size":vsize,
            "availability_zone": "nova",
            "source_volid": "null",
            "description": vdesc,
            "multiattach ": "false",
            "snapshot_id": "null",
            "name": vname,
            "imageRef": "null",
            "volume_type": "lvmdriver-1",
            "metadata": {},
            "source_replica": "null",
            "consistencygroup_id":"null"
        }
    }
        headers = {'X-Auth-Token':token,'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
    return render(request, 'app/addvolume.html', {})
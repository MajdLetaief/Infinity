from django.shortcuts import render
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
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

    token = request.session['X-Token']
    projectid = request.session['X-Project']
    url = "http://192.168.114.130:8776/v3/" + projectid + "/volumes"
    if request.POST:
        vname = request.POST['vname']
        vsize = request.POST['vsize']
        vdesc = request.POST['vdesc']
        f = "false"
        data = {
        "volume": {
            "size":vsize,
            "availability_zone": "nova",
            "description": vdesc,
            "multiattach ": f,
            "name": vname,
            "volume_type": "lvmdriver-1",
            "metadata": {},
        }
    }
        headers = {'X-Auth-Token':token,'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
    return render(request, 'app/addvolume.html', {})



def ImageView(request):
    urlImage = "http://192.168.114.130:9292/v2/images"
    s = request.session['X-Token']
    l = {'X-Auth-Token': s}
    i = requests.get(urlImage, headers=l)
    ListImages = i.json()
    images = ListImages['images']

    if request.POST:
        token = request.session['X-Token']
        url = "http://192.168.114.130:9292/v2/images/" + i.Id
        headers = {'X-Auth-Token': token, 'content-type': 'application/json'}
        requests.post(url, headers=headers)
        return render(request, 'app/images.html')

    return render(request, 'app/images.html', {"images":images})


def addImageView(request):
    token = request.session['X-Token']
    url = "http://192.168.114.130:9292/v2/images"
    if request.POST:
        container_format = request.POST['container_format']
        disk_format = request.POST['disk_format']
        name = request.POST['name']
        data = {

                "container_format": container_format,
                "disk_format": disk_format,
                "name": name,
        }
        headers = {'X-Auth-Token': token, 'content-type': 'application/json'}
        requests.post(url, data=json.dumps(data), headers=headers)



    return render(request, 'app/addimages.html', {})

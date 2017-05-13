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
    status=ListImages["images"][0]["status"]
    name = ListImages["images"][0]["name"]
    format = ListImages["images"][0]["disk_format"]
    id = ListImages["images"][0]["id"]
    container_format = ListImages["images"][0]["container_format"]

    return render(request, 'app/images.html', {"status": status,
                                               "name":name,
                                               "disk":format,
                                               "id":id,
                                               "container_format":container_format})

def FlavorsView(request):
    if request.POST:
        urlAddingFlavor = "http://192.168.114.130:8774/v2.1/flavors"
        token = request.session['X-Token']
        newHeader = {'X-Auth-Token':token,'content-type': 'application/json'}
        name = request.POST['name']
        ram = request.POST['ram']
        vcpus = request.POST['vcpus']
        disk = request.POST['disk']
        newFlavor = {
            "flavor":{
                "name":name,
                "ram":ram,
                "vcpus":vcpus,
                "disk":disk,
            }
        }
        addingFlavorResponse = requests.post(urlAddingFlavor, data=json.dumps(newFlavor), headers=newHeader)
        print(addingFlavorResponse.status_code)
        print(addingFlavorResponse.text)
    urlFlavors = "http://192.168.114.130:8774/v2.1/flavors"
    token = request.session['X-Token']
    newHeader = {'X-Auth-Token' : token}
    flavorsListResponse = requests.get(urlFlavors, headers=newHeader)
    flavorsListJson = flavorsListResponse.json()
    flavors = flavorsListJson['flavors']
    return render(request, 'app/flavors.html', {'flavors':flavors})

def FlavorView(request,flavorId):
    urlFlavor = "http://192.168.114.130:8774/v2.1/flavors/"+flavorId
    token = request.session['X-Token']
    newHeader = {'X-Auth-Token':token}
    oneFlavorResponse = requests.get(urlFlavor, headers = newHeader)
    oneFlavorJson = oneFlavorResponse.json()
    flavor = oneFlavorJson['flavor']
    return render(request, 'app/flavor.html', {'flavor':flavor})

def AddFlavorView(request):
    return render(request, 'app/flavorForm.html' , {})

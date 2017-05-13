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



def GetNetwork(request):
    urlNetwork = "http://192.168.114.130:9696/v2.0/networks"
    s = request.session['X-Token']
    l = {'X-Auth-Token': s}
    i = requests.get(urlNetwork, headers=l)
    ListNetworks = i.json()
    status = ListNetworks["networks"]

    print(i.json())
    return render(request, 'app/networks.html', {"status": status})

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

def AddNetworkView(request):

    token = request.session['X-Token']
    projectid = request.session['X-Project']
    url = "http://192.168.114.130:9696/v2.0/networks"
    if request.POST:
        nname = request.POST['nname']
        f = "true"
        data = {
    "network": {
        "name": nname,
        "admin_state_up": f

    }
}
        headers = {'X-Auth-Token':token,'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
    return render(request, 'app/addNetwork.html', {})

def FipView(request):
    s = request.session['X-Token']
    l = {'X-Auth-Token': s}
    urlfip = "http://192.168.114.130:9696/v2.0/floatingips"
    i = requests.get(urlfip, headers=l)
    Listfip = i.json()
    fips=Listfip['floatingips']
    return render(request, 'app/fip.html', {'fips':fips})


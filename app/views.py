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
    return render(request, 'app/volume.html', {})

def GetNetwork(request):
    urlNetwork = "http://192.168.114.130:9696/v2.0/networks"
    s = request.session['X-Token']
    l = {'X-Auth-Token': s}
    i = requests.get(urlNetwork, headers=l)
    ListNetworks = i.json()
    status = ListNetworks["networks"]

    print(i.json())
    return render(request, 'app/networks.html', {"status": status})


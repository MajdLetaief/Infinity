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
        request.session['X-Token']= r.headers.get('X-Subject-Token')
        print(r.headers.get('X-Subject-Token'))
        print(r.text)


    return render(request, 'app/index.html', {})


def LoginView(request):

        # return render()
    return render(request, 'app/login.html', {})

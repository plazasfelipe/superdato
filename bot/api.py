import os
import json
import requests

url = os.environ['API_URL']

headers = {
  'Content-Type': 'application/json'
}

def post_response(user, date, response):
    event = {'user':user, 'date':date, 'response':response}
    payload = json.dumps(event)
    response = requests.request("POST", url+'events', headers=headers, data=payload)

def get_topics():
    payload = {}
    response = requests.request("GET", url+'topics', headers=headers, data=payload)
    response_serialize = json.loads(response.text)
    data = response_serialize['data']

    return data

def get_insight(topic):
    try:
        payload = json.dumps({'topic':topic})
        response = requests.request("GET", url+'insights', headers=headers, data=payload)
        response_serialize = json.loads(response.text)
        data = response_serialize['data']
        insight = data['insight']
        graph = data['graph']

        return insight, graph
    except:
        pass

def get_terms():
    payload = {}
    response = requests.request("GET", url+'terms', headers=headers, data=payload)
    response_serialize = json.loads(response.text)
    data = response_serialize['data']

    return data

def get_insight_by_terms(terms):
    payload = json.dumps({'terms':terms})
    response = requests.request("GET", url+'insight-by-term', headers=headers, data=payload)
    response_serialize = json.loads(response.text)
    data = response_serialize['data']
    insight = data[0]['insight']

    return insight


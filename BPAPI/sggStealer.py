import requests

import ujson as json

baseURL = 'https://api.smash.gg/'

def _getJSON(url):
    r = requests.get(url)
    try:
        data = r.json()
        return data['entities']
    except:
        print('Could not parse json from: {}'.format(url))

def _getSet(setID):
    url = '{}/set/{}?expand[]=games'.format(baseURL, setID)
    data = _getJSON(url)
    print(data)
    return data

def _getPlayer(playerID):
    url = '{}player/{}'.format(baseURL, playerID)
    return _getJSON(url)

def _getPhase(phaseID):
    url = '{}/phase/{}'.format(baseURL, phaseID)
    return _getJSON(url)

def _getPhaseGroup(phaseGroupID):
    url = '{}/phase_group/{}?expand[]=standings&expand[]=sets'.format(baseURL, phaseGroupID)
    data = _getJSON(url)
    return data

def _getTournament(tournamentSlug):
    url = '{}tournament/{}?expand[]=event&expand[]=groups'.format(baseURL, tournamentSlug)
    return _getJSON(url)


def getAllSets(tournamentSlug):
    tData = _getTournament(tournamentSlug)
    phase_groups = tData['groups']
    sets = []
    for phase_group in phase_groups:
        pgData = _getPhaseGroup(phase_group['id'])
        for set in pgData['sets']:
            sets.append(set)
            if set['games']:
                print(set['games'])
    return sets

if __name__ == '__main__':
    x = getAllSets('genesis-5')
    with open('test.json', 'w') as outf:
        json.dump(x, outf)


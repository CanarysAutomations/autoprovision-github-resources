from requests import put
from termcolor import colored
from json import dumps
def provideTeamAccess(inputObject, head, csvReader):
    print()
    print( "Give repository access to a team")
    print( "=================================")
    try:
        for r in csvReader:
            teamname = r['Team'].replace(' ','-')
            repopermission = r['Permissions']
            repobody = {
                'permission' : repopermission
            }
            give_team_access_req_url = 'https://api.github.com/orgs/' + inputObject.Organization + '/teams/' + teamname.lower() + '/repos/' + inputObject.Organization + '/' + inputObject.RepoName
            put(give_team_access_req_url, headers=head, data=dumps(repobody))
            team_newname = teamname.upper()
            repo_newname = inputObject.RepoName.upper()
            print('Team',team_newname,'has been given',repopermission,'to',repo_newname)
    except:
        print(colored("Unable to provide access for {}".format(teamname.upper()),'red'))
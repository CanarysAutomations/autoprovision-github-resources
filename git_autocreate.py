from stdiomask import getpass
from requests import post
from requests import put
from json import dumps
from termcolor import colored
from csv import DictReader

print("   _____ _ _   _   _       _            ___        _              _____                _     " )
print("  |  __ (_) | | | | |     | |          / _ \      | |            /  __ \              | |    ")
print("  | |  \/_| |_| |_| |_   _| |__ ______/ /_\ \_   _| |_ ___ ______| /  \/_ __ ___  __ _| |_ ___")
print("  | | __| | __|  _  | | | | '_ \______|  _  | | | | __/ _ \______| |   | '__/ _ \/ _` | __/ _ \\")
print("  | |_\ \ | |_| | | | |_| | |_) |     | | | | |_| | || (_) |     | \__/\ | |  __/ (_| | ||  __/")
print("   \____/_|\__\_| |_/\__,_|_.__/      \_| |_/\__,_|\__\___/       \____/_|  \___|\__,_|\__\___|")
print()
PATToken = '' #getpass('GitHub Token: ')
Organization = 'GHAPITesting' #input('GitHub Organization: ')
RepoName = 'test_grenston' #input('Repository Name: ')
Repository_Visibility = 'private' #input('Repository Visibility: ')
RepoDescription = 'A sample description' #input('Add the Repository Description: ')
# ProjectName = input('Project to be created for the Repository: ')
# Columns = input('Project Column Names to be Created: ')
CsvSource = './testcsv.csv' #input('CSV Source: ')

csvReader = DictReader(open(CsvSource))
if Repository_Visibility == 'public':
    type='public'
else:
    type='private'

head = {
    'Authorization' : 'Bearer ' + PATToken,
    'Accept' : 'application/vnd.github.nebula-preview+json;application/vnd.github.inertia-preview+json'
}

RepoDetails = {
    'name':RepoName,
    'description':RepoDescription,
    'visibility':type
}

print()
print( "Create repository in organization")
print( "=================================")

req_url = 'https://api.github.com/orgs/' + Organization + '/repos'
try:
    gitobject= post(url=req_url, headers=head, data=dumps(RepoDetails))
    repository_name = gitobject.json()['name']
    print()
    print(repository_name,'repository is created') 

except Exception as e:
    print(colored("Unable to Create Repository:",'red'),colored(e,'red'))

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
        req_url2 = 'https://api.github.com/orgs/' + Organization + '/teams' + teamname + '/repos' + Organization + '/' + RepoName
        gitobject_2 = put(url=req_url2, headers=head, data=dumps(repobody))
        team_newname = teamname.upper()
        repo_newname = RepoName.upper()
        print('Team',team_newname,'has been given',repopermission,'to',repo_newname)
except Exception as e:
    print(colored("Unable to Provide Repository Access:",'red'),colored(e,'red'))
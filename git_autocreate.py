from stdiomask import getpass
import requests
from json import dumps
from termcolor import colored
print("   _____ _ _   _   _       _            ___        _              _____                _     " )
print("  |  __ (_) | | | | |     | |          / _ \      | |            /  __ \              | |    ")
print("  | |  \/_| |_| |_| |_   _| |__ ______/ /_\ \_   _| |_ ___ ______| /  \/_ __ ___  __ _| |_ ___")
print("  | | __| | __|  _  | | | | '_ \______|  _  | | | | __/ _ \______| |   | '__/ _ \/ _` | __/ _ \\")
print("  | |_\ \ | |_| | | | |_| | |_) |     | | | | |_| | || (_) |     | \__/\ | |  __/ (_| | ||  __/")
print("   \____/_|\__\_| |_/\__,_|_.__/      \_| |_/\__,_|\__\___/       \____/_|  \___|\__,_|\__\___|")
print()
PATToken = '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' #getpass('GitHub Token: ')
Organization = 'GHAPITesting' #input('GitHub Organization: ')
RepoName = 'test_grenston' #input('Repository Name: ')
Repository_Visibility = 'private' #input('Repository Visibility: ')
RepoDescription = 'A sample description' #input('Add the Repository Description: ')
# ProjectName = input('Project to be created for the Repository: ')
# Columns = input('Project Column Names to be Created: ')
# ExcelSourceDir = input('Excel Source: ')
# WorkSheetName = input('Specify the worksheet name: ')

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

req_url = 'https://api.github.com/orgs/' + Organization + '/repos'
try:
    gitobject= requests.post(url=req_url, headers=head, data=dumps(RepoDetails))
    repository_name = gitobject
    print()
    print(gitobject.json()['name'],'repository is created') 

except Exception as e:
    print(colored("Unable to Create Repository:",'red'),colored(e,'red'))

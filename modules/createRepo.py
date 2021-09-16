from termcolor import colored
from requests import post
from json import dumps
def createRepo(inputObject, head, type):
    RepoDetails = {
        'name':inputObject.RepoName,
        'description':inputObject.RepoDescription,
        'visibility':type
    }

    print()
    print( "Create repository in organization")
    print( "=================================")

    create_repo_req_url = 'https://api.github.com/orgs/' + inputObject.Organization + '/repos'
    try:
        create_repo_response = post(url=create_repo_req_url, headers=head, data=dumps(RepoDetails))
        repository_name = create_repo_response.json()['name']
        print()
        print(repository_name,'repository is created') 

    except:
        print(colored(create_repo_response.json(),'red'))
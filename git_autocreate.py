from modules.initialise import initialiseInputs
from sys import argv
from json import dumps
from requests import post
from requests import put
from termcolor import colored


print("   _____ _ _   _   _       _            ___        _              _____                _     " )
print("  |  __ (_) | | | | |     | |          / _ \      | |            /  __ \              | |    ")
print("  | |  \/_| |_| |_| |_   _| |__ ______/ /_\ \_   _| |_ ___ ______| /  \/_ __ ___  __ _| |_ ___")
print("  | | __| | __|  _  | | | | '_ \______|  _  | | | | __/ _ \______| |   | '__/ _ \/ _` | __/ _ \\")
print("  | |_\ \ | |_| | | | |_| | |_) |     | | | | |_| | || (_) |     | \__/\ | |  __/ (_| | ||  __/")
print("   \____/_|\__\_| |_/\__,_|_.__/      \_| |_/\__,_|\__\___/       \____/_|  \___|\__,_|\__\___|")
print()


argumentList = argv[1:]
initialisedValues = initialiseInputs(argumentList)
inputObject, head, csvReader, type = initialisedValues['inputObject'], initialisedValues['head'], initialisedValues['csvReader'], initialisedValues['type']
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
        give_team_access_response = put(give_team_access_req_url, headers=head, data=dumps(repobody))
        team_newname = teamname.upper()
        repo_newname = inputObject.RepoName.upper()
        print('Team',team_newname,'has been given',repopermission,'to',repo_newname)
except:
    print(colored("Unable to provide access for {}".format(teamname.upper()),'red'))

if not inputObject.ProjectName or not inputObject.Columns:
    print("\nProject Name or Columns not Specified. Skipping Project Creation\n")
else:
    projectdetails = {
        'name' : inputObject.ProjectName,
        'body': 'created for repo ' + inputObject.RepoName
    }

    try:
        print()
        print("Create a project for the repository")
        print("===================================")
        create_project_req_url = 'https://api.github.com/repos/' + inputObject.Organization + '/' + inputObject.RepoName + '/projects'
        create_project_response = post(url=create_project_req_url, headers=head, data=dumps(projectdetails))
        print(inputObject.ProjectName,"Project is Created")
    except:
        print(colored(create_project_response.json(),'red'))
    else:
        ColumnNames = inputObject.Columns.split(',')
        projectID = create_project_response.json()['id']
        create_columns_req_url = 'https://api.github.com/projects/' + str(projectID) + '/columns'
        try:
            for c in ColumnNames:
                ColumnParams = { 'name' : c }
                create_columns_response = post(url=create_columns_req_url, headers=head, data=dumps(ColumnParams))
            print("Project Columns are added\n") 
        except:
            print(colored(create_columns_response.json(),'red'))


        
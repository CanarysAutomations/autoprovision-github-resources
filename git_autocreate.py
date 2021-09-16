from getopt import getopt
from sys import argv
from json import dumps
from csv import DictReader
from stdiomask import getpass
from requests import post
from requests import put
from termcolor import colored
from sys import exit

print("   _____ _ _   _   _       _            ___        _              _____                _     " )
print("  |  __ (_) | | | | |     | |          / _ \      | |            /  __ \              | |    ")
print("  | |  \/_| |_| |_| |_   _| |__ ______/ /_\ \_   _| |_ ___ ______| /  \/_ __ ___  __ _| |_ ___")
print("  | | __| | __|  _  | | | | '_ \______|  _  | | | | __/ _ \______| |   | '__/ _ \/ _` | __/ _ \\")
print("  | |_\ \ | |_| | | | |_| | |_) |     | | | | |_| | || (_) |     | \__/\ | |  __/ (_| | ||  __/")
print("   \____/_|\__\_| |_/\__,_|_.__/      \_| |_/\__,_|\__\___/       \____/_|  \___|\__,_|\__\___|")
print()
class inputClass:
    def __init__ (self, argumentList=None):
        if not argumentList:
            self.PATToken = getpass('GitHub Token: ')
            self.Organization = input('GitHub Organization: ')
            self.RepoName = input('Repository Name: ')
            self.Repository_Visibility = input('Repository Visibility: ')
            self.RepoDescription = input('Add the Repository Description: ')
            self.ProjectName = input('Project to be created for the Repository. Press ENTER if not required: ')
            if self.ProjectName != "":
                self.Columns = input('Project Column Names to be Created: ')
            else:
                self.Columns = ""
            self.CsvSource = input('CSV Source (Use / for path separator): ')
        else:           
            if len(argumentList) == 16:
                options = "t:o:r:v:d:p:c:f:"
                long_options = ["Token =", "Organization =","Repository =", "Visibility =","Description =","Project =","Columns =","File ="]
                arguments, values = getopt(argumentList, options, long_options)
                for currentArgument, currentValue in arguments:
                    if currentArgument in ("-p", "--Project "):
                        self.ProjectName = currentValue
                    elif currentArgument in ("-c", "--Columns "):
                        self.Columns = currentValue
            else:
                options = "t:o:r:v:d:f:"
                long_options = ["Token =", "Organization =","Repository =", "Visibility =","Description =","File ="]
                self.Columns = None
                self.ProjectName = None
            arguments, values = getopt(argumentList, options, long_options)
            for currentArgument, currentValue in arguments:
                if currentArgument in ("-t", "--Token "):
                    self.PATToken = currentValue                
                elif currentArgument in ("-o", "--Organization "):
                    self.Organization = currentValue               
                elif currentArgument in ("-r", "--Repository "):
                    self.RepoName = currentValue
                elif currentArgument in ("-v", "--Visibility "):
                    self.Repository_Visibility = currentValue
                elif currentArgument in ("-d", "--Description "):
                    self.RepoDescription = currentValue
                elif currentArgument in ("-f", "--File "):
                    self.CsvSource = currentValue


def initialiseInputs(argumentList):
    if len(argumentList) == 0:
        inputObject = inputClass()
    elif len(argumentList) != 16 and len(argumentList) != 12:
        print("Refer README for unattended usage. Supports only 6 or 8 arguments.")
        choice = input("Enter \"Y\" to input values manually: ")
        if (choice.upper() == "Y"):
            inputObject = inputClass()
        else:
            exit("Aborting.......")
    elif len(argumentList) == 16:
        if set(["-t","-o","-r","-v","-d","-p","-c","-f"]) <= set(argumentList) or set(["--Token ", "--Organization ","--Repository ", "--Visibility ","--Description ","--Project ","--Columns ","--File "]) <= set(argumentList):
            inputObject = inputClass(argumentList)
        else:
            print("Refer README for unattended usage. Proper arguments not provided.")
            choice = input("Enter \"Y\" to input values manually: ")
            if (choice.upper() == "Y"):
                inputObject = inputClass()
            else:
                exit("Aborting.......")
    else:
        if set(['-t','-o','-r','-v','-d','-f']) <= set(argumentList) or set(["--Token ", "--Organization ","--Repository ", "--Visibility ","--Description ","--File "]) <= set(argumentList):
            inputObject = inputClass(argumentList) 
        else: 
            print("Refer README for unattended usage. Proper arguments not provided.")
            choice = input("Enter \"Y\" to input values manually: ")
            if (choice.upper() == "Y"):
                inputObject = inputClass()
            else:
                exit("Aborting.......")
            
    csvReader = DictReader(open(inputObject.CsvSource))
    if inputObject.Repository_Visibility == 'public':
        type = 'public'
    elif inputObject.Repository_Visibility == 'internal':
        type = 'internal'
    else:
        type='private'

    head = {
        'Authorization' : 'Bearer ' + inputObject.PATToken,
        'Accept' : 'application/vnd.github.v3+json;application/vnd.github.nebula-preview+json;application/vnd.github.inertia-preview+json'
    }
    returnValues = {'inputObject':inputObject,'head':head,'csvReader':csvReader,'type':type}
    return returnValues

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


        
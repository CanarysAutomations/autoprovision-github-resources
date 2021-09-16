from json import dumps
from requests import post
from termcolor import colored

def createProject(inputObject, head):   
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
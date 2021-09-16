'''
The tool will communicate with the repositories and organizations of GitHub. The exe will be available for auto provision of GitHub resources with each release. 
This tool is intended to restrict manual labour as much as possible. The tool with the help of few inputs will:
    1. Create a repository - An empty repository will be created
    2. Repository Access - The teams will be given access to the created repository based on the csv file input
    3. Project - An empty project will be created for the repository with the Columns defined by the user.
'''

from modules.title import showTitle
from modules.initialise import initialiseInputs
from modules.createRepo import createRepo
from modules.teamAccess import provideTeamAccess
from modules.createProject import createProject
from sys import argv

argumentList = argv[1:]
initialisedValues = initialiseInputs(argumentList)
inputObject, head, csvReader, type = initialisedValues['inputObject'], initialisedValues['head'], initialisedValues['csvReader'], initialisedValues['type']

showTitle()
createRepo(inputObject, head, type)
provideTeamAccess(inputObject, head, csvReader)
if not inputObject.ProjectName or not inputObject.Columns:
    print("\nProject Name or Columns not Specified. Skipping Project Creation\n")
else:
    createProject(inputObject, head)     
from modules.initialise import initialiseInputs
from modules.createRepo import createRepo
from modules.teamAccess import provideTeamAccess
from modules.createProject import createProject
from sys import argv

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
createRepo(inputObject, head, type)
provideTeamAccess(inputObject, head, csvReader)
if not inputObject.ProjectName or not inputObject.Columns:
    print("\nProject Name or Columns not Specified. Skipping Project Creation\n")
else:
    createProject(inputObject, head)


        
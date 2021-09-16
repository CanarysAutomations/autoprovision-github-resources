from sys import exit
from getopt import getopt
from stdiomask import getpass
from csv import DictReader

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
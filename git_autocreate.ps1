#param(
#[Parameter(Mandatory=$true)][string]$UserToken = "Default",
#[string]$Organization = "Default",
#[string]$RepoName ="Default",
#[string]$RepoDescription = "Default",
#[string]$RepoPermission = "Default",
#[string]$ProjectName ="Default",
#[string[]]$Teams = @(),
#[string[]]$Columns = @('ToDo','InProgress','Done'))

[string[]] $TeamNames= @()
[string[]] $Columns= @()

$UserToken = Read-Host -Prompt 'Input your GitHub Token'
$Organization = Read-Host -Prompt 'Input your GitHub Organization'
$RepoName = Read-Host -Prompt 'Input your Repository Name'
$RepoDescription = Read-Host -Prompt 'Add the Repository Description'
$RepoPermission = Read-Host -Prompt 'Add the Repo Permissions to be given'
$TeamNames = Read-Host -Prompt 'Add the teams to provide the repository access'
$ProjectName = Read-Host -Prompt 'Give the Project Name for the Repository'
$Columns = Read-Host -Prompt 'Provide the Project Column Names to be Created'




$head = @{

    Authorization = 'Bearer ' + $UserToken

}

$projectheader=@{

    Authorization = 'Bearer ' + $UserToken
    Accept="application/vnd.github.inertia-preview+json"

}


$RepoDetails = @{

    name=$RepoName
    description=$RepoDescription

}

$body = $RepoDetails | ConvertTo-Json

$createreporequest=@{

        Uri = "https://api.github.com/orgs/$Organization/repos" 
        Method = "Post"
        body = $body 
        ContentType = "application/json"
        Headers = $head

}

$gitobject= Invoke-RestMethod @createreporequest

Write-Host
Write-Host  "Give repository access to a team"
Write-Host  "================================"

Write-Host "`n"("Repository Created " + $gitobject.name)

$repo=$gitobject.name

$repoparams=@{

    permission=$RepoPermission

}

$repobody=$repoparams | ConvertTo-Json

$Teams=$TeamNames.split(',')

foreach($i in $Teams)
{

    $team = $i.ToLower();

    $teamname = $team -replace ' ','-'

    $repoaccessrequest=@{

            Uri = "https://api.github.com/orgs/$Organization/teams/$teamname/repos/$Organization/$repo" 
            Method = "PUT"
            body = $repobody 
            ContentType = "application/json"
            Headers = $head

    }

    $gitobject_2= Invoke-RestMethod @repoaccessrequest

    Write-Host "`n"("Team " + $teamname + " Has been given Access to " + "$RepoName")
}

Write-Host 
Write-Host   "Create a project for the repository"
Write-Host   "==================================="

$projectparams=@{

    name=$ProjectName
    body="created for repo "+$repo

}

$projectdetails = $projectparams | ConvertTo-Json

$createprojectrequest=@{

        Uri = "https://api.github.com/repos/$Organization/$repo/projects" 
        Method = "Post"
        body = $projectdetails
        ContentType = "application/json"
        Headers = $projectheader

}

$gitObject_3= Invoke-RestMethod @createprojectrequest

Write-Host "`n"($ProjectName + " Project is Created")
Write-Host

Write-Host  "Adding the project Columns"
Write-Host  "=========================="
Write-Host

#$Columns=@('ToDo','InProgress','Done')

$projectID = $gitObject_3.id

$ColumnNames = $Columns.split(',')

foreach($j IN $ColumnNames)
{

        $Columnparams=@{name=$j}

        $Columnnames = $Columnparams | ConvertTo-Json

        $createprojectcolumnrequest=@{

            Uri = "https://api.github.com/projects/$projectID/columns" 
            Method = "Post"
            body = $Columnnames
            ContentType = "application/json"
            Headers = $projectheader

        }

        $gitObject_4= Invoke-RestMethod @createprojectcolumnrequest

}

 Write-Host  "Project Columns are added" 
 Write-Host 


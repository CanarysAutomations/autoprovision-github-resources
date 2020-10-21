param(
#[Parameter(Mandatory=$true)][string]$entserver = "Default",
[Parameter(Mandatory=$true)][string]$UserToken = "Default",
[string]$Organization = "Default",
[string]$RepoName ="Default",
[string]$RepoDescription = "Default",
[string]$RepoPermission = "Default",
[string]$ProjectName ="Default",
[string]$Teamname = "Default")

$head = @{

    Authorization = 'Bearer ' + $UserToken

}

$projectheader=@{

    Authorization = 'Bearer ' + $UserToken
    Accept="application/vnd.github.inertia-preview+json"

}

#$Userlist = @('EAAdmin','OSS-Dev')

$hash = @{

    name=$RepoName
    description=$RepoDescription

}

$body = $hash | ConvertTo-Json

$createreporequest=@{

        Uri = "https://api.github.com/orgs/$Organization/repos" 
        Method = "Post"
        body = $body 
        ContentType = "application/json"
        Headers = $head

}

$gitobject= Invoke-RestMethod @createreporequest

Write-Host  "Give repository access to a team"
Write-Host  "================================"

Write-Host "`n"("Repository Created " + $gitobject.name)

$repo=$gitobject.name

$repoparams=@{

    permission=$RepoPermission

}

$repobody=$repoparams | ConvertTo-Json

$team = $Teamname.ToLower();

$repoaccessrequest=@{

        Uri = "https://api.github.com/orgs/$Organization/teams/$team/repos/$Organization/$repo" 
        Method = "PUT"
        body = $repobody 
        ContentType = "application/json"
        Headers = $head

}

$gitobject_2= Invoke-RestMethod @repoaccessrequest

Write-Host "`n"("Team " + $TeamName + " Has been given Access to " + "$RepoName")

Write-Host   "Create a project for the repository"
Write-Host   "==================================="

$projectparams=@{

    name=$ProjectName
    body="created for repo"+$repo

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

Write-Host  "Adding the project Columns"
Write-Host  "=========================="

$Columns=@('ToDo','InProgress','Done')

$projectID = $gitObject_3.id

Write-Host $projectID

foreach($j IN $Columns)
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

        $gitObject3= Invoke-RestMethod @createprojectcolumnrequest

}

Write-Host "Project Columns are added" 


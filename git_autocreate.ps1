
Write-Host                  "   _____ _ _   _   _       _            ___        _              _____                _     "  
Write-Host                  "  |  __ (_) | | | | |     | |          / _ \      | |            /  __ \              | |    "  
Write-Host                  "  | |  \/_| |_| |_| |_   _| |__ ______/ /_\ \_   _| |_ ___ ______| /  \/_ __ ___  __ _| |_ ___" 
Write-Host                  "  | | __| | __|  _  | | | | '_ \______|  _  | | | | __/ _ \______| |   | '__/ _ \/ _` | __/ _ \"
Write-Host                  "  | |_\ \ | |_| | | | |_| | |_) |     | | | | |_| | || (_) |     | \__/\ | |  __/ (_| | ||  __/"
Write-Host                  "   \____/_|\__\_| |_/\__,_|_.__/      \_| |_/\__,_|\__\___/       \____/_|  \___|\__,_|\__\___|"
Write-Host                                                                                             
                                                                                             


[string[]] $TeamNames= @()
[string[]] $Columns= @()

$PATToken = Read-Host -Prompt 'GitHub Token' -AsSecureString
$Organization = Read-Host -Prompt 'GitHub Organization'
$RepoName = Read-Host -Prompt 'Repository Name'
$Repository_Visibility = Read-Host -Prompt 'Repository Visibility'
$RepoDescription = Read-Host -Prompt 'Add the Repository Description'
$ProjectName = Read-Host -Prompt 'Project to be created for the Repository'
$Columns = Read-Host -Prompt 'Project Column Names to be Created'
$ExcelSourceDir = Read-Host -Prompt 'Excel Source'
$WorkSheetName = Read-Host -Prompt 'Specify the worksheet name'

if($Repository_Visibility -eq "public")
{
    $type="public"
}else{
    $type="private"
}

$UserToken =[Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($PATToken))

$excel = New-Object -com Excel.Application

$wbook = $excel.workbooks.open($ExcelSourceDir)


$worksheet = $wbook.Worksheets.Item($WorkSheetName)

$maxrows = ($worksheet.UsedRange.Rows).Count

$wbobject = New-Object -TypeName psobject
$wbobject | Add-Member -MemberType NoteProperty -Name Team -Value $null
$wbobject | Add-Member -MemberType NoteProperty -Name Permissions -Value $null


$head = @{

    Authorization = 'Bearer ' + $UserToken
    Accept="application/vnd.github.nebula-preview+json"

}

$projectheader=@{

    Authorization = 'Bearer ' + $UserToken
    Accept="application/vnd.github.inertia-preview+json"

}


$RepoDetails = @{

    name=$RepoName
    description=$RepoDescription
    visibility=$type

}

$body = $RepoDetails | ConvertTo-Json

$createreporequest=@{

        Uri = "https://api.github.com/orgs/$Organization/repos" 
        Method = "Post"
        body = $body 
        ContentType = "application/json"
        Headers = $head

}

try {

    $gitobject= Invoke-RestMethod @createreporequest



    $repository_name = $gitobject.name.ToUpper()


    Write-host
    Write-Host "$repository_name repository is created " 

}catch{

     Write-Host "Unable to Create Repository:" $_.Exception.Response.StatusDescription  -ForegroundColor Red

}

Write-Host
Write-Host "Give repository access to a team"
Write-Host "================================"


$repo=$gitobject.name

try {

    for ($i = 2; $i -le $maxrows; $i++)
    {
        $wbobject.Team = $worksheet.Cells.item($i,1).Text.ToLower();
	    $wbobject.Permissions = $worksheet.Cells.item($i,2).Text.ToLower();

        $repository = $repo
        $team = $wbobject.Team
        $repopermission = $wbobject.Permissions

        $teamname = $team -replace ' ','-'
	
	    $repoparams=@{

            permission=$repopermission

        }

	    $repobody=$repoparams | ConvertTo-Json

        $repoaccessrequest=@{

            Uri = "https://api.github.com/orgs/$Organization/teams/$teamname/repos/$Organization/$repository" 
            Method = "PUT"
            body = $repobody 
            ContentType = "application/json"
            Headers = $head

        }

        $gitobject_2= Invoke-RestMethod @repoaccessrequest

        $team_newname = $team.ToUpper()
        $repo_newname = $repo.ToUpper()

        Write-Host "Team $team_newname has been given $repopermission to $repo_newname"
    }
}catch {

     Write-Host "Unable to Provide Repository Access:" $_.Exception.Response.StatusDescription  -ForegroundColor Red
}

Write-Host 
Write-Host "Create a project for the repository"
Write-Host "==================================="

if (!$ProjectName -and !$ColumnNames)
{
    Write-Host "Project Name or Columns not Specified. Skipping Project Creation"

} else {

    $projectparams=@{

        name=$ProjectName
        body="created for repo "+$repo

    }

    $projectdetails = $projectparams | ConvertTo-Json

    try{

            $createprojectrequest=@{

                Uri = "https://api.github.com/repos/$Organization/$repo/projects" 
                Method = "Post"
                body = $projectdetails
                ContentType = "application/json"
                Headers = $projectheader

            }

            $gitObject_3= Invoke-RestMethod @createprojectrequest

            Write-Host "$ProjectName Project is Created"
            Write-Host

       }catch{

         Write-Host "Unable to Create the Repository Project:" $_.Exception.Response.StatusDescription  -ForegroundColor Red

       }

    Write-Host "Adding the project Columns"
    Write-Host "=========================="
    Write-Host


    $projectID = $gitObject_3.id

    $ColumnNames = $Columns.Split(',')

    try {

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

        Write-Host "Project Columns are added" 
        Write-Host 

     }catch{

         Write-Host "Unable to Create the Requested Project Columns:" $_.Exception.Response.StatusDescription  -ForegroundColor Red

       }

 }


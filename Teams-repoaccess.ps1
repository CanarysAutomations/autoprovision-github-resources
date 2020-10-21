param(
[string]$UserToken="Default",
[string]$Organization="Default",
[string]$ExcelSourceDir="Default",
[string]$WorkSheetName = "Default")

$head = @{
Authorization = 'Bearer ' + $UserToken
Accept ="application/vnd.github.nebula-preview+json"
}

#$ExcelSourceDir = "D:\team_permissions.xlsx"
#$WorkSheetName = "Sheet1"

$excel = New-Object -com Excel.Application

$wbook = $excel.workbooks.open($ExcelSourceDir)


$worksheet = $wbook.Worksheets.Item($WorkSheetName)

$maxrows = ($worksheet.UsedRange.Rows).Count

$wbobject = New-Object -TypeName psobject
$wbobject | Add-Member -MemberType NoteProperty -Name Team -Value $null
$wbobject | Add-Member -MemberType NoteProperty -Name Repository -Value $null
$wbobject | Add-Member -MemberType NoteProperty -Name Permissions -Value $null

for ($i = 2; $i -le $maxrows; $i++)
{
    $wbobject.Team = $worksheet.Cells.item($i,1).Text.ToLower();
    $wbobject.Repository = $worksheet.Cells.item($i,2).Text.ToLower();
    $wbobject.Permissions = $worksheet.Cells.item($i,3).Text.ToLower();

    $repo = $wbobject.Repository
    $team = $wbobject.Team
    $repopermission = $wbobject.Permissions

    $repoparams=@{

         permission=$repopermission

       }

    $newteamname = $team -replace ' ','-'
    
    $body=$repoparams | ConvertTo-Json

    $teamsaccesstoreposrequest=@{

        Uri = "https://api.github.com/orgs/$Organization/teams/$newteamname/repos/$Organization/$repo" 
        Method = "PUT"
        body = $body 
        ContentType = "application/json"
        Headers = $head

    }

    $gitObject= Invoke-RestMethod @teamsaccesstoreposrequest

}


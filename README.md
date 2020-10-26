# Autoprovision ⚙ GitHub Resources

The tool will communicate with the repositories and organizations of GitHub. The [exe](https://github.com/CanarysAutomations/autocreate-github-resources/releases) will be available for auto provision of GitHub resources with each release. This tool is intended to restrict manual labour as much as possible. The tool with the help of few inputs will  

- **Create a repository**- An empty repository will be created

- **Repository Access**- The teams will be given access to the created repository based on the excel file input

- **Project**- An empty project will be created for the repository with a pre-configured **Basic Kanban** template with columns for **To Do**, **In progress**, and **Done**

## Benefits

- This tool can be used as a template when repositories have to be created for an organization
- Automate the creation of repositories with very few inputs

## GitHub REST API

The endpoints used in the tool are GitHub's Rest API v3. A series of endpoints are made available by GitHub to alter resources like repositories, teams, projects and make organization level changes. For further reading on the GitHub's REST API please [click here](https://docs.github.com/en/free-pro-team@latest/rest/overview)

## Prerequisites

- Only current organisational teams will be considered
- Admin access to the organization for creating the repositories
- Excel File with Team Names and permissions
- GitHub PAT Token must be authorized to access the required organization

## Download :arrow_down:

Download the tool from [here](https://github.com/CanarysAutomations/autoprovision-github-resources/releases).

## Usage Instructions :memo:

For instructions on how to use the tool, please [click here](https://github.com/CanarysAutomations/autocreate-github-resources/wiki)

## Current Tool Limitations  :x: :x:

- In the future, GitHub could change its remaining endpoints used in the tool without warning

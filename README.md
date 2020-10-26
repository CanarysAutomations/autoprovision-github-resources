## Auto-Create GitHub Resources

The tool will communicate with the repositories and organisations of GitHub. With each release, the exe file to auto build GitHub resources, will be available. The purpose of this tool is to limit manual work as much as possible. The tool with the help of few inputs will  

#### Create a repository

An empty repository will be created

#### Repository Access

Based on the excel file input, the teams will be given access to the created repository 

#### Project 

An Empty project will be created for the repository with a basic kanban board.


### Advantages

- This tool can be used as a template when repositories have to be created for an organization.
- Automate your repository creation with very few inputs

## GitHub REST API

The endpoints used in the tool are GitHub's Rest API v3. A series of endpoints are made available by GitHub to alter resources like repositories, teams, projects and make organization level changes. For further reading on the GitHub's REST API please [click here](https://docs.github.com/en/free-pro-team@latest/rest/overview)

## Prerequisites

- only existing teams in the organization will be considered
- Admin access to the organization for creating the repositories
- Excel File with Team Names and permissions
- GitHub PAT Token must be authorized to access the required organization

## Usage Instructions :memo:

For instructions on how to use the tool, please [click here](https://github.com/CanarysAutomations/autocreate-github-resources/wiki)

## Current Tool Limitations  :x: :x:

- GitHub might change its rest endpoints used in the tool without notice in future

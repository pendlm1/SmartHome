# TEAM 5 CAPSTONE PROJECT



## Communication

 [Check out the [Microsoft Teams Setup](https://teams.microsoft.com/_#/school/conversations/General?threadId=19:5e7e69657bbb4065a697642f8c087472@thread.tacv2&ctx=channel)]
 - To edit the README.md file, checkout
 [this page](https://help.github.com/en/articles/basic-writing-and-formatting-syntax#lists)
 for formatting.
 
## Project Prerequisites
- Familiarity using Git
- Basic Knowledge of how databases work
- Proficientcy in Python

## Project Setup 

1. Fork this Repository by clicking the "Fork" icon above.
2. Go to your fork and clone it to the desired location on your
local machine using the command:
   - ```git clone https://your_fork.link```
3. Configure source repo as an upstream using:
   - ```git remote add upstream [Upstream git URL]```

## Workflow Conventions
To contribute to the project, see the following list of instructions in order to add a
feature/merge it into the master. (**__Note:__** These instructions are mainly for
public branches and don't apply to any local branches/test versions of the project.)


1. Before creating a branch locally, ensure your current branch is `master` using `git branch`.
2. Create branch using `git branch BRANCH_NAME`.
   - If branch is a feature, prefix the branch name with `feat-`.
   (Example: `feat-BRANCH_NAME`)
   - If branch is a fix, prefix branch name with `fix-`.
   (Example: `fix-BRANCH_NAME`)
   - If branch is an update, prefix branch name with `update-`.
   (Example: `update-BRANCH_NAME`)
3. Once you're satisfied with your local branch changes, commit them and push them to your fork
using the commands below:
   - `git add -A` (Adds all local changes to be committed)
     - or `git add CHANGE_NAME` (Adds changes one by one given name as arg)
   - `git commit` (commits changes locally)
     - Note: requires commit message using Vim. [See
     [Tutorial](https://www.fprintf.net/vimCheatSheet.html)]. Try to describe with a little detail
     what you did with every commit.
   - `git push` (will push your code to the current working branch)
     - If it's your first time pushing code to this branch you'll have to set the branch up on your
     fork using the command `git push --set-upstream origin NAME_OF_BRANCH`.
4. Finally, you can merge this branch to your Fork's `master` branch and then issue a **Merge Request**
via the **Merge Requests** Tab on the left. 


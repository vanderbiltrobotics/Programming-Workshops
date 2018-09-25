# Git & GitHub (9.25.18)

### Git & Version Control

When you're working on a complicated piece of code, it's very easy to introduce small bugs that are difficult to track down. It's especially easy when new features are constantly being added or when multiple people are working on the same code. One way to try and solve this is to manually save copies of all your files periodically so that you can revert back to previous versions when something breaks. But while this ensures that you always have a working version of your code saved somewhere, it still has lots of drawbacks
- Manually saving copies of all your files is very tedious, especially for big projects with lots of files
- This doesn't make it any easier for multiple people to work on the same project
- Just having an older version that works doesn't necessarily make it easy to figure out why the new version doesn't work

**Git** is a *version-control* tool which solves each of these issues. Git makes it easy to maintain previous versions of code, compare different versions, and to coordinate work on a project between a group of people. If used properly, git will allow our team to ensure that there is always a deployable, working version of our code while at the same time letting us work on new features and improvements to existing ones. 

Git is super common in industry and also very useful for personal projects and school, so it's a good idea to get familiar with it now. 

#### Setup

[Install git here](https://git-scm.com/downloads)

[Documentation for git commands here](https://git-scm.com/docs)

Udacity has a very thorough series of videos on git & GitHub - [this YouTube playlist](https://www.youtube.com/watch?v=Ytux4IOAR_s&list=PLAwxTw4SYaPk8_-6IGxJtD3i2QAu5_s_p&index=1) has all the videos

#### Repository

A set of files being tracked by git is called a repository. If a folder contains a git repository, it will have a .git folder (you'll need to view hidden files to see this). This folder is put there when the repository is initialized and is where git will store all version history of your code. You will never need to access this file, just know that's where git is storing everything.

To create a git repository use the command `git init`. This will either create a new folder that contains a new git repository or it will add a repositiry to the current directory.

There are three main parts to a local repository: The workspace, the staging area, and the .git directory

The *workspace* or 'working directory' is what you can see when you open the folder. This has all the files from the version of the code you're currently working on. If you make changes to files and save them, these are the files that are modified. 

The *staging area* is simply an index that lets git know which files in the workspace it should be keeping track of. Initially, this is empty, but you'll add to it all the files that you want tracked. 

The *.git directory* is where all the versions of your project are saved. When you make a commit (discussed in the next section), a 'snapshot' of all the files in the staging area is saved here.


#### Commits

A commit is just a single version of your project that has been saved by git. Every time you 'make a commit,' the current state of all the files being tracked by git (the files that have been added to the staging area) is saved in the repository. The basic process for making a commit is as follows

1. Create or modify files in the workspace
2. Add those files to the staging area (`git add [FILENAME]` will do this)
3. Continue working on those files until you've reached a logical checkpoint
4. Commit the changes to those files (`git commit -m "Brief commit message explaining what you've changed"`)

Once you've added a file to the staging area, it'll stay there until you explicitly remove it from the staging area (`git reset HEAD [FILENAME]`) so you don't need to re-add the file before every subsequent commit. 

Here are a few useful git commands related to commits
- `git status` - this will show you what files in the working directory have been modified since the last commit and whether or not those files are in the staging area. It's useful to check this before committing so you can see exactly what changes will be saved in the commit.
- `git log` - this will show basic information about the last few commits such as the ID, the author of the commit, the commit message, and the time of the commit
- `git diff COMMIT_ID_1 COMMIT_ID_2` - this will list all the differences between the two commits specified. This can be really useful for tracking down a small bug. It will list any lines that changed and how they changed. If you leave the COMMIT_ID fields blank, git will diff the two most recent commits.

#### Remote

Now that we've covered the basics of committing in a local repository, what if we want to work on our repository with someone else or backup our files online? To do this, we need to create something called a 'remote.' A remote is a copy of our repository that is stored somewhere on the Internet. If your repository has a remote, it **a)** is backed up somewhere other than your computer and  **b)** can be accessed by multiple people if those people know where the remote is. GitHub is a website that hosts remote reopsitories for people, making it easy for teams to collaborate on a project. 

Here the basic commands for setting up remotes
- `git add remote origin www.url_where_remote_is_located.com` - this creates a remote called 'origin' (this is the standard name to use if your project has one remote) at the url specified. This lets your local repository know that there's a repository at that url which you want to use as a remote and that you're using 'origin' to refer to that remote
- `git remote set-url origin www.new_url_for_origin_remotet.com` - this changes the url associated with the remote 'origin' to the url specified

#### Cloning

Often, there will be an existing repository, perhaps stored on GitHub, that we want to start working on ourselves. We need to create a local copy of the repository (so that the files and commit history are available on our computer to work on) and we need to add the location where the code is currently being stored as a remote (so that other people using the code can see our changes when we make them). With git, the combination of these two steps is called 'cloning'

`git clone www.url_of_existing_repository.com` copies the repository at the specified url into the current folder and adds that url as a remote (called 'origin'). When you start working on the codebase for the robot, the first thing you should do is clone the repository you want to work on. That way you can make commits and push the commits back up to GitHub so that the rest of the team can see and build off the changes you made.  

#### Push / Pull

Now we have a remote repository associated with our local one. If we make changes to our local repository (by making commits), we need a way to update the remote repository with those changes. This is called 'pushing' the changes to the remote.

The command `git push origin` will send all of the new commits on the current branch of our local repository (more on branches shortly) to the corresponding branch on the 'origin' remote. Immediately following a succesful push, the current branch in the local repository and the corresponding branch in the remote repository should be identical.

Now say that someone else has a copy of our repository on their computer, makes some commits, and pushes those commits to the remote. When we go to work on the code on our computer, we may want to update our repoository with those changes before we start working. Updating our current repository with the contents of the remote is called 'pulling'

The command `git pull origin` updates the local repository with any new commits from the remote repository. 

#### Merging

It's easy to think of situations where problems could arise as different people push / pull. What if 'person A' pushes makes a change to a file and commits it, and meanwhile, 'person B' has made a different change to that same file. When person B goes tries to push his commit, there will be a conflict. 

There are two steps that must be taken to resolve this. First, git requires you to have pulled the most recent version of a remote before you can push to it. In the situation above, person B's local repository is one commit behind the remote, so they will have to pull before they can push. If the changes that person A made concerned different files than person B's changes or even unrelated parts of the same files, git will simple update the relevant files in person B's repository. But if person A and person B both made changes to the same parts of a file, git will require person B to 'merge' the changes in a new commit before they can push to the remote. 

When a pull conflict occurs, git will add both people's changes to the files in person B's workspace as well as some markings (>>>>>>>>>>>>, <<<<<<<<<<<<<) to indicate where in the files these conflicts occurred. It's person B's job to go through the conflicting areas and resolve the differences. Once they have done so, they make a new commit (which should explain that it is a merge in the commit description) and push that commit to the remote. The conflict is now resolved. 

#### Branching

Say we have a working version of the code for our robot that does an okay job at mining gravel. We have an idea for a way to improve the control code for the digging mechanism so that the robot will do a really good job mining gravel. However, this is going to be a complicated change and will likely mean the code will be broken for a while until everything is implemented. This is a situation where we should use 'branching'. 

By default, every repository has one branch, the 'master' branch. If we create a new branch, any commits we make on that branch will not effect other branches at all. This gives us a good way to work on new features safely while ensuring that there's always a working version of our code on the master branch. Once we've finished the feature on the new branch and tested it thoroughly to be sure that it works as expected, we can merge this branch with the master branch. This merge process is exactly the same as what was described earlier. If there any conflicts between the two branches, we'll have to resolve them. Once everything has been resolved, we commit the merge. After merging, both branches still exist, they just refer to exactly the same thing. 

A key to understanding commits and branches is realizing that a branch is just a 'label' for a particular commit. Imagine an arrow between every commit and the commit that came before it. When we commit on a particular branch, we add a new commit that 'points' to the previous commit, and we move the 'label' of the current branch to that new commit. When create a new branch, we also add a new commit pointing to the previous commit. However, rather than moving the label for the old branch to this new commit, we create a new label and give it to the new commit. Thus, the two branches will always share some common ancestor but will develop separately from that point. When two branches are merged, we create a new commit that points to *both* of the 'labeled' commits, the latest commit on each branch. Both labels now advance to this new commit and thus both branches are now the same. The commit history of the combined branch includes all the commits from each of the merged branches.

### GitHub

GitHub is a web service built around git which allows users to store repositories online. While it's possible to make commits directly on GitHub, this functionality is limited. GitHub is generally used to host remotes for projects. Anyone can clone a repository from GitHub on to their local system, and if given push access, can push changes they make back to the version hosted on GitHub. This allows teams to collaborate by providing a common remote that all team members can pull from / push to. Additionally, open-source projects can put their code on GitHub, allowing any interested member of the community to clone that code, work on improvements, and request that those changes be incorporated into the official source code (see Forking & Pull Requests below). 

### How are we using Git & GitHub for our team

Our team will be using a few different repositories throughout the year, each of which is hosted on GitHub. Any member who needs to work on the code can simplly clone the latest version (or pull if they've already done that) and then work on whatever they need to work on. We'll be using branching to ensure that a working version of the code is always available on the master branch (if the competition were today, that's the code that we'd use) while improvements can be developed safely on other branches. 

The repositories you should be aware of are described below:
 [COMING SOON!!]

### Other interesting git / GitHub functionality

#### Forking

#### Pull requests


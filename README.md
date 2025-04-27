# SimpleDockerProject (UNFINISHED)
Project to display a simple HELLO WORLD page inside of a Container (This will work on Ubuntu/Debian Based Distros of Linux)

1. Update Linux (sudo apt update)
2. Upgrade Linux (sudo apt upgrade)
3. Install docker (sudo apt install docker)
4. Install docker compose (sudo apt install docker compose)

5. Install Nano (sudo apt install nano)
6. Install Pip (sudo apt install pip)
7.  Upgrade Pip (sudo pip install --upgrade pip)

8. Create docker-Projects directory (mkdir docker-projects)
9. Change directory to docker-projects (cd /docker-projects)
    #ALL FILES WILL BE CREATED IN SAME DIRECTORY (docker-projects) 
  
12. Create file "app.py" for Python Web application (touch app.py)
13. Copy & paste code from GitHub file "app.py" located in Github Repo
14. Open app.py and copy & paste code (sudo nano app.py)
    After copy & paste hit CTRL+X to save and type Y or Yes to confirm
    
15. Create text file for app dependencies (touch requirements.txt)
16. Open requirements.txt file & add dependencies
    (sudo nano requirements.txt) #when you type this it should open a text file
     Line 1 ---> Flask
     Line 2 ---> redis
     Hit CTRL+X to save and type Y or Yes to confirm

13 Create dockerfile (touch dockerfile)

14 Copy & paste code from Github File "dockerfile" located in Github Repo

15 Open "dockerfile" and copy & paste code (sudo nano dockerfile)
   After copy & paste hit CTRL+X to save and type Y or Yes to confirm

16. Create "docker-compose.yml" file (touch docker-compose.yml)
    
18. Open "docker-compose.yml" file and copy & paste code (sudo nano touch)
    Copy & Paste code from "docker-compose.yml) file located in Github Repo
    After Copy & Paste hit CTRL+X to save and type Y or YES to confirm
    #BE AWARE THAT YAML FILES ARE VERY SENSITIVE TO INDENTATION, SPACES, & SYNTAX. USE A.I TO CORRECT IT IF NECESSARY

19. Make sure you are still in "docker-projects" directory (cd /docker-projects)
    #THE COMMAND IN THE NEXT STEP DOESN'T WORK UNLESS YOU ARE IN "DOCKER-PROJECTS" DIR

20. Run command to start building the images & containers (sudo docker-compose up --build)

21. After commands finish running your container should be built.
    Go to "http://localhost:5000" on your web browser
    You should see a message "Hello World! You have visited 1 times"
    #Refreshing the page will add to visitor count

23. To stop or break down container after you are done (sudo docker-compose down)

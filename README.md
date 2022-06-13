Created with Python 3.8.2
Port = 5000

**INSTALL COMMANDS**
1. Create a virtual environment and install requirements (`pip3 install -r requirements.txt`)
2. `deactivate` your virtual environment and navigate to the root project folder
3. Run `./bootstrap.sh` command from the root directory
4. Once the flask server is running, enter curl commands in the following format to access API (ex.: `curl http://localhost:5000/api/posts -d "tags=history,tech&sortBy=likes&sortOrder=desc"`)
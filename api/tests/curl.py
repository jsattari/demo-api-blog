import os
# os.system("./bootstrap.sh & ")

tests = """
# ping
curl -I http://localhost:5000/ping
# get history and tech blogs
curl http://localhost:5000/api/posts -d "tags=history,tech&sortBy=likes&sortOrder=desc"
# No params but tags
curl http://localhost:5000/api/posts -d "tags=history"
# no params
curl http://localhost:5000/api/posts -d "tags="
"""

for line in tests.strip().split('\n'):
    if not line.startswith('#'):
        cmd = line.strip() 
        os.system(cmd)
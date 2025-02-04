from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import json
import dotenv as env
import os
import time

from starlette.responses import HTMLResponse

env.load_dotenv()

envpassword = os.getenv("PASSWORD")

f = open('owen.json')
data = json.load(f)

def getdata():
    return data

def history():
    history = data['history']
    return history

def current():
    current = data['current']
    return current

def started():
    started = data['started']
    return started

def checkpassword(password):
    if str(envpassword) == str(password):
        return True

def set(action):
    if data['current'] != "":
        data['history'].append({"action": data['current'], "timeStarted": data['started']})

    data['current'] = action
    data['started'] = round(time.time())
app = FastAPI()

docs = {
    "/history (GET)": "view recent actions of Owen",
    "/set/{password}/{action} (GET)": "For Owen to set his action, password locked",
    "/help (GET)": "this screen, shows commands",
    "/get (POST)": "search for an action, takes json: {action: String (Optional), time: Int (Optional)}, if nothing specified, returns action history",
    "/current (GET)": "get Owen's current action"
}

class Action(BaseModel):
    action: Optional[str]
    time: Optional[int] = None

html = '''
<!DOCTYPE html>
<html>
<h1>Owen's API</h1>
<body>

An API for tracking exactly what Owen is doing... constantly...
It's not creepy I promise.

<h2>Access</h2>
Server is accessible at: owen-action-api.vercel.app

<h2>Commands</h2>
<ul>

- /help (GET) - get a list of commands
<p>
- /set/{password}/{action} (GET)** - For Owen to set his current action, you don't get the password!
</p>
<p>
- /history (GET) - Get a history of all action, complete with timestamps {"history": [Actions]}
</p>
<p>
- /get (POST) - Get an action based on time or name: {"action": String, "time": Int (Unix Time)}
</p>
<p>
- /current (GET) - Get Owen's current action {"current": "{action}"}
</p>
</body>
</html>
'''
@app.get("/")
async def root():
    return HTMLResponse(html)

@app.get("/history")
async def history():
    if history():
        return {"history": data.history()}
    else:
        return {"error": "No history found"}

@app.get("/help")
async def help():
    return docs

@app.get("/set/{password}/{action}")
async def setaction(password: str, action: str):
    if checkpassword(password):
        set(action)
        return {"success": True, "data": getdata()}
    else:
        return {"error": "Invalid password"}

@app.post("/get")
async def get(action: Action):
    if action:
        for i in data['history']:
            if i['action'] == action.action or i['time'] == action.time:
                return {"success": True, "data": i}
            else:
                return {"error": "Invalid action", "action": action}
    else:
        return {"history": history()}

@app.get("/current")
async def getcurrent():
    if current():
        return {"current": current()}
    else:
        return {"error": "Invalid action"}
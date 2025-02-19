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

f = open('data.json')
data = json.load(f)
f.close()

def checkpassword(password):
    return str(envpassword) == str(password)

def setaction(action):
    if data['current'] != "":
        data['history'].append({"action": data['current'], "timeStarted": data['started']})

    data['current'] = action
    data['started'] = round(time.time())

    f = open('data.json', 'w')
    f.write(json.dumps(data))
    f.close()

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
<a href="https://owen-action-api.vercel.app">Server</a>
<br />
<a href="https://github.com/ojsrb/OwenAPI">GitHub</a>

<h2>Commands</h2>

<ul>
<li> /help (GET) - get a list of commands </li>

<li> /set/{password}/{action} (GET) - For Owen to set his current action, you don't get the password! </li>

<li> /history (GET) - Get a history of all action, complete with timestamps {"history": [Actions]} </li>

<li> /get (POST) - Get an action based on time or name: {"action": String, "time": Int (Unix Time)} </li>

<li> /current (GET) - Get Owen's current action {"current": "{action}"} </li>
</ul>

</body>
</html>
'''
@app.get("/")
async def root():
    return HTMLResponse(html)

@app.get("/history")
async def history():
    if data['history'] != []:
        return {"history": data['history']}
    else:
        return {"error": "No history found"}

@app.get("/help")
async def help():
    return docs

@app.get("/set/{password}/{action}")
async def set(password: str, action: str):
    if checkpassword(password):
        setaction(action)
        return {"success": True, "data": data}
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
        return {"history": data['history']}

@app.get("/current")
async def getcurrent():
    if data['current'] != "":
        return {"current": data['current'], "time": data['started']}
    else:
        return {"current": "None"}
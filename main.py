from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import json
import dotenv as env
import os
import time

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

@app.get("/")
async def root():
    return {"Welcome to the Owen API! Use '/help' for reference."}

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
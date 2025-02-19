Owen's API

An API for tracking exactly what Owen is doing... constantly...
It's not creepy I promise.

#### Access
Server is accessible at owen-action-api.vercel.app

### GET
```
- /help - get a list of commands
- /set/{password}/{action} - For Owen to set his current action, you don't get the password!
- /history - Get a history of all action, complete with timestamps {"history": [Actions]}
- /current - Get Owen's current action {"current": "{action}"}
```
### POST
```
- /get - Get an action based on time or name: {"action": String, "time": Int (Unix Epoch)}
```

### Setup
This is built with FastAPI using the following commands:
```
git clone https://github.com/ojsrb/ActionAPI.git
cd OwenAPI
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev main.py
```

### Notes

For RaspAPI Reviewers, you won't be able to access /set because you do not have the password. This is what it does return when you DO have the password. 

<img width="301" alt="Screenshot 2025-02-18 at 9 56 54 AM" src="https://github.com/user-attachments/assets/9d4629b3-d21b-48a8-9a27-935ec73db69f" />

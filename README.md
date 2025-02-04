Owen's API

An API for tracking exactly what Owen is doing... constantly...
It's not creepy I promise.

#### Access
Server is accessible at: 

### Commands

- /help (GET) - get a list of commands
- /set/{password}/{action} (GET) - For Owen to set his current action, you don't get the password!
- /history (GET) - Get a history of all action, complete with timestamps
- /get (POST) - Get an action based on time or name: {"action": String, "time": Int (Unix Time)}
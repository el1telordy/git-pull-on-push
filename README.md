# git-pull-on-push
Simple tool to automate "git pull" on a remote machine using GitHub Webhook

## Installation
1. Clone repo `git clone https://github.com/el1telordy/git-pull-on-push.git`
2. `cd git-pull-on-push`
3. Install the dependencies `pip install -r requirements.txt`
4. Create Webhook on GitHub. Pick "application/json" as the Content type and generate Secret. Payload URL is your `<host_address>:<port_address>/github-webhook`
5. Edit **config.py** manually
6. Launch main.py `nohup python3 main.py &`

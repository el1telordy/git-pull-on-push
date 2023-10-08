from flask import Flask, request
from hashlib import sha256
import git
import config
import hmac
import logging

app = Flask(__name__)
repo = git.Repo(config.repo_dir)

logging.basicConfig(filename=config.log_file, filemode='a', format='%(asctime)s, %(message)s', level=logging.INFO)
logger = logging.getLogger('git-pull-on-push')

@app.route("/github-webhook", methods=["POST"])

def handleRequest():
  event_type = request.headers.get('X-GitHub-Event')
  secret_hash = request.headers.get('X-Hub-Signature-256')
  payload = request.data

  if(request.headers.get('content-type') != 'application/json'): 
    logger.warning("Request with incorrect content-type")
    return "Incorrect payload type", 415

  if(secret_hash == None):
    logger.warning("Request without secret")
    return "Secret not provided", 401

  if(verifySecret(payload, secret_hash) is False):
    logger.warning("Request with incorrect secret")
    return "Incorrect secret", 401

  if(event_type == 'ping'):
    logger.info("Ping request")
    return "Pong", 200

  if(event_type == 'push'):
    repo.remotes.origin.pull()
    logger.info("Pulled from repository")
    return "Success", 200

  logger.warning("Incorrect request")
  return "Incorrect request provided", 400

def verifySecret(payload, hash):
  hash_obj = hmac.new(config.secret.encode('utf-8'), msg=payload, digestmod=sha256)
  expected_hash = "sha256=" + hash_obj.hexdigest()
  if hmac.compare_digest(expected_hash, hash):
    return True
  else:
    return False

if __name__ == "__main__":
  app.run(host=config.host_address, port=config.app_port)

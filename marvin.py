#!/usr/bin/env python3
import couchdb
import os
from dotenv import dotenv_values

###########
# WARNING #
###########
# Using this script uses a lot of resources since it fetches all your
# documents! An example of OK usage is running this once every evening to get a
# list of tasks you completed on that day. An example of bad usage is running
# it in your bash prompt. Improper usage may result in disabling your API
# access or even terminating your Marvin account. Don't worry, we'll give you a
# warning first (via your Marvin email address), but please do be careful for
# the sake of other users.

if os.path.exists(".env.development"):
  config = dotenv_values(".env.development")
else:
  config = dotenv_values(".env")

syncServer = config["SYNC_SERVER"]
syncDatabase = config["SYNC_DATABASE"]
syncUser = config["SYNC_USER"]
syncPassword = config["SYNC_PASSWORD"]

print(syncServer)
if syncUser == "":
  print("Populate the .env file with your credentials (Strategies -> API -> View credentials)")
  exit(1)

couch = couchdb.Server(f"https://{syncUser}:{syncPassword}@{syncServer}")

db = couch[syncDatabase]
tasks = []
for row in db.view("_all_docs", include_docs=True):
  doc = row.doc

  if "db" in doc and doc["db"] == "Tasks" and not ("_deleted" in doc and doc["_deleted"]):
    tasks.append(row)

print(f"Found {len(tasks)} tasks")

# 代码生成时间: 2025-09-19 07:08:32
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Data Backup and Restore Script using Bottle framework.
This script provides a simple web service for backing up and restoring data.
"""

from bottle import Bottle, request, response, run
import json
import os
import shutil
import tarfile
import datetime

# Initialize Bottle app
app = Bottle()

# Configuration
BACKUP_DIR = "./backups"
DATA_DIR = "./data"

# Ensure backup directory exists
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Helper function to create a backup
def create_backup():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    backup_file = f"{BACKUP_DIR}/backup-{timestamp}.tar.gz"
    with tarfile.open(backup_file, "w:gz") as tar:
        tar.add(DATA_DIR)
    return backup_file

# Helper function to restore from a backup
def restore_backup(backup_file):
    with tarfile.open(backup_file, "r:gz") as tar:
        tar.extractall(DATA_DIR)

# API endpoint for creating a backup
@app.route("/backup", method="POST")
def backup():
    try:
        backup_file = create_backup()
        return {"status": "success", "message": f"Backup created: {backup_file}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# API endpoint for restoring data
@app.route("/restore", method="POST")
def restore():
    backup_file = request.json.get("backup_file")
    try:
        if not os.path.exists(backup_file):
            return {"status": "error", "message": "Backup file not found"}
        restore_backup(backup_file)
        return {"status": "success", "message": "Data restored successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Run the Bottle app
if __name__ == "__main__":
    run(app, host="localhost", port=8080, debug=True)

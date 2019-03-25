import os, subprocess, requests, datetime
from subprocess import call
from app import app, db
from app.models import Student, Course, Admin, Mac, Location, Receiver

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Admin': Admin}
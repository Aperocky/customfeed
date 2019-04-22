import os, sys
sys.path.append("..")
from feed import Feeder
import time
from flask import Flask
from flask import render_template, request, session, redirect, jsonify
import threading

feeder = Feeder()
app = Flask(__name__, template_folder='templates')

def runfeeder():
    print("RUNNING FEEDER FOR {}th TIME".format(feeder.test_counter))
    feeder.crawl()
    feeder.purge()
    feeder.set_priority()
    feeder.test()

def feedworker():
    print("STARTING FEEDWORKER")
    while True:
        runfeeder()
        time.sleep(60)

def runbackground():
    feeder_thread = threading.Thread(target=feedworker)
    feeder_thread.daemon = True
    feeder_thread.start()

# Test end point
@app.route("/rest", methods=["GET"])
def jsonlist():
    queue = feeder.sortedqueue()
    return jsonify(queue)

if __name__ == "__main__":
    runbackground()
    app.run(debug=True, use_reloader=False)

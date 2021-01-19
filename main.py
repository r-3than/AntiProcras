from flask import Flask, render_template ,redirect,request
import threading
import time , platform
from datetime import datetime as dt
global update
update = False

app = Flask(__name__)
@app.route("/")
def index():
    f = open("blockedpages.txt").read().split("\n")
    return render_template("index.html",webpages=f)

@app.route("/remove/<webname>")
def removeWeb(webname):
    global update
    f = open("blockedpages.txt").read().split("\n")
    try:f.remove(webname)
    except: print("Webpage not found")
    outdata = ""
    for item in f:
        outdata = outdata+item+"\n"
    outdata = outdata[:-1]
    Out = open("blockedpages.txt","w")
    Out.write(outdata)
    Out.close()
    update = True
    return redirect("/websites/")

@app.route("/websites/",methods = ['POST', 'GET'])
def websites():
    global update
    if request.method == 'POST':
        user = request.form['websitename']
        f = open("blockedpages.txt","a")
        f.write("\n"+user)
        f.close()
        update = True
    f = open("blockedpages.txt").read().split("\n")
    return render_template("websites.html",webpages=f)

@app.route("/workhours/",methods = ['POST', 'GET'])
def workhours():
    global update
    if request.method == 'POST':
        start = request.form['starthour']
        end = request.form['endhour']
        f = open("state.txt","w")
        f.write(start+"|"+end+"|1")
        f.close()
        update = True
    f = open("blockedpages.txt").read().split("\n")
    s = open("state.txt").read().split("|")
    return render_template("workhours.html",webpages=f,startHour=s[0],endHour=s[1])

@app.route("/controlpanel/",methods = ['POST', 'GET'])
def controlpanel():
    f = open("blockedpages.txt").read().split("\n")
    return render_template("controlpanel.html",webpages=f)


@app.route("/view/<page>")
def viewPage(page):
    page = "http://"+page
    return redirect(page)

@app.route("/add/")
def addWeb():
    return redirect("/")




def block_websites():
    global update
    update = True
    Linux_host = "/etc/hosts"
    Window_host = """C:\Windows\System32\drivers\etc\hosts"""
    if platform.system() == "Linux":
        default_hoster = Linux_host
    else:
        default_hoster = Window_host
    redirect = "127.0.0.1"
    while True:
        if update:
            sites_to_block = open("blockedpages.txt").read().split("\n")
            f = open("state.txt").read().split("|")
            start_hour = int(f[0])
            end_hour = int(f[1])
            print("A")
            update = False
        if dt(dt.now().year, dt.now().month, dt.now().day,start_hour)< dt.now() < dt(dt.now().year, dt.now().month, dt.now().day,end_hour): 
            with open(default_hoster, 'r+') as hostfile:
                hosts = hostfile.read()
                for site in  sites_to_block:
                    if site not in hosts:
                       hostfile.write(redirect+' '+site+'\n')
        else:
            with open(default_hoster, 'r+') as hostfile:
                hosts = hostfile.readlines()
                hostfile.seek(0)
                for host in hosts:
                    if not any(site in host for site in sites_to_block):
                        hostfile.write(host)
                hostfile.truncate()
        time.sleep(10)



if __name__ == '__main__':
    watcher = threading.Thread(target=block_websites).start()
    app.run(port=5002,debug=True)

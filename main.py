from flask import Flask, render_template ,redirect,request
import threading
import time, platform
import datetime
import ctypes, sys
global update
global sites
global times 
sites = open("blockedpages.txt").read().split("\n")
times = open("state.txt").read().split("|")
update = False

app = Flask(__name__)
@app.route("/")
def index():
    global sites
    f = sites
    return render_template("index.html",webpages=f)

@app.route("/remove/<webname>")
def removeWeb(webname):
    global update
    global sites
    f = sites
    try:f.remove(webname)
    except: print("Webpage not found")
    outdata = ""
    for item in f:
        outdata = outdata+item+"\n"
    outdata = outdata[:-1]
    Out = open("blockedpages.txt","w")
    Out.write(outdata)
    Out.close()
    removeSite(webname)
    update = True
    return redirect("/websites/")

@app.route("/websites/",methods = ['POST', 'GET'])
def websites():
    global update
    global sites
    if request.method == 'POST':
        user = request.form['websitename']
        sites.append(user)
        f = open("blockedpages.txt","a")
        f.write("\n"+user)
        f.close()
        update = True
    f = sites
    return render_template("websites.html",webpages=f)

@app.route("/workhours/",methods = ['POST', 'GET'])
def workhours():
    global update
    global times
    global sites
    if request.method == 'POST':
        start = request.form['starthour']
        end = request.form['endhour']
        f = open("state.txt","w")
        f.write(start+"|"+end+"|1")
        f.close()
        times = [start,end,1]
        update = True
    f = sites
    s = times
    return render_template("workhours.html",webpages=f,startHour=s[0],endHour=s[1])

@app.route("/controlpanel/",methods = ['POST', 'GET'])
def controlpanel():
    global sites
    f = sites
    return render_template("controlpanel.html",webpages=f)


@app.route("/view/<page>")
def viewPage(page):
    page = "http://"+page
    return redirect(page)

@app.route("/add/")
def addWeb():
    return redirect("/")



def is_time_between(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:
        return check_time >= begin_time or check_time <= end_time



def removeSite(website):
    sites_to_block = [website]
    Linux_host = "/etc/hosts"
    Window_host = """C:\Windows\System32\drivers\etc\hosts"""
    if platform.system() == "Linux":
        default_hoster = Linux_host
    else:
        default_hoster = Window_host
    with open(default_hoster, 'r+') as hostfile:
                hosts = hostfile.readlines()
                hostfile.seek(0)
                for host in hosts:
                    if not any(site in host for site in sites_to_block):
                        hostfile.write(host)
                hostfile.truncate()



def block_websites():
    global update
    global sites
    global times
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
            sites_to_block = sites
            start_hour = int(times[0])
            end_hour = int(times[1])
            print("update!")
            update = False
        if is_time_between(datetime.time(start_hour,0), datetime.time(end_hour,00)): 
            print("BLOCK!")
            print(sites_to_block)
            with open(default_hoster, 'r+') as hostfile:
                hosts = hostfile.read()
                for site in  sites_to_block:
                    if site != '':
                        if site not in hosts:
                            hostfile.write(redirect+'\t'+site+'\n')
        else:
            print("UNLOCK")
            with open(default_hoster, 'r+') as hostfile:
                hosts = hostfile.readlines()
                hostfile.seek(0)
                for host in hosts:
                    if not any(site in host for site in sites_to_block):
                        hostfile.write(host)
                hostfile.truncate()
        time.sleep(3)




def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    if platform.system() == "Windows":
        if is_admin():
            watcher = threading.Thread(target=block_websites).start()
            app.run(port=5002,debug=False)
        else:
    # Re-run the program with admin rights
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:

        #watcher = threading.Thread(target=block_websites).start()
        watcher = threading.Thread(target=block_websites).start()
        app.run(port=80,debug=False)

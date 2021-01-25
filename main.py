from flask import Flask, render_template ,redirect,request
import threading
import time, platform
import datetime
import ctypes, sys
import string , random

def get_random_string(length):
    sample_letters = string.ascii_letters + string.digits + "|\/?.,<>#@;:{}[]-=+_`"
    result_str = ''.join((random.choice(sample_letters) for i in range(length)))
    return result_str


class AntiPro:
    def __init__(self):
        self.sites = open("blockedpages.txt").read().split("\n")
        self.times = open("state.txt").read().split("|")
        self.code = get_random_string(64)
        Linux_host = "/etc/hosts"
        Window_host = """C:\Windows\System32\drivers\etc\hosts"""
        if platform.system() == "Linux":
            default_hoster = Linux_host
        else:
            default_hoster = Window_host
        self.default_hoster = default_hoster
        self.allowChange = False
        self.update = False
        self.running = True
        self.timeamt = 5
        self.count = 0
    def block_websites(self):
        
        timecheck = 5
        self.update = True
        redirect = "127.0.0.1"
        while self.running:
            if self.allowChange:
                self.count = self.count+timecheck
            #print(count,self.timeamt,self.allowChange)
            if self.count > self.timeamt:
                self.count = 0
                self.allowChange = False
            if self.update:
                sites_to_block = self.sites
                start_hour = int(self.times[0])
                end_hour = int(self.times[1])
                print("update!")
                self.update = False
            if is_time_between(datetime.time(start_hour,0), datetime.time(end_hour,00)): 
                print("BLOCK!")
                print(sites_to_block)
                with open(self.default_hoster, 'r+') as hostfile:
                    hosts = hostfile.read()
                    for site in  sites_to_block:
                        if site != '':
                            if site not in hosts:
                                hostfile.write(redirect+'\t'+site+'\n')
            else:
                print("UNLOCK")
                with open(self.default_hoster, 'r+') as hostfile:
                    hosts = hostfile.readlines()
                    hostfile.seek(0)
                    for host in hosts:
                        if not any(site in host for site in sites_to_block):
                            hostfile.write(host)
                    hostfile.truncate()
            time.sleep(timecheck)
    def removePage(self,webname):
        if self.allowChange:
            try:self.sites.remove(webname)
            except: print("Webpage not found")
            outdata = ""
            for item in self.sites:
                outdata = outdata+item+"\n"
            outdata = outdata[:-1]
            Out = open("blockedpages.txt","w")
            Out.write(outdata)
            Out.close()
            sites_to_block = [webname]

            with open(self.default_hoster, 'r+') as hostfile:
                        hosts = hostfile.readlines()
                        hostfile.seek(0)
                        for host in hosts:
                            if not any(site in host for site in sites_to_block):
                                hostfile.write(host)
                        hostfile.truncate()
        return self.sites
    def addPage(self,webname):
        self.sites.append(webname)
        f = open("blockedpages.txt","a")
        f.write("\n"+webname)
        f.close()
        self.update = True
        return self.sites
    def unlockall(self):
        if self.allowChange:
            sites_to_block = self.sites
            with open(self.default_hoster, 'r+') as hostfile:
                        hosts = hostfile.readlines()
                        hostfile.seek(0)
                        for host in hosts:
                            if not any(site in host for site in sites_to_block):
                                hostfile.write(host)
                        hostfile.truncate()
    def setHours(self,start,end):
        if self.allowChange:
            f = open("state.txt","w")
            f.write(start+"|"+end+"|1")
            f.close()
            self.times = [start,end,1]
            self.update = True
    def getCode(self):
        if is_time_between(datetime.time(int(self.times[0]),0), datetime.time(int(self.times[1]),00)): 
            self.code = get_random_string(32)
        else:
            self.code = "entered correctly"
            self.timeamt = 60*5
            self.allowChange = True
        return self.code
    def checkCode(self,code):
        if self.code == code:
            self.code = "entered correctly"
            self.timeamt = 60*5
            self.allowChange = True
    def getTimes(self):
        return self.times
    def getSites(self):
        return self.sites
    def on(self):
        self.running = True
        self.watcher = threading.Thread(target=self.block_websites).start()
    def off(self):
        self.running = False
        self.update = False
        self.unlockall()

AP = AntiPro()
app = Flask(__name__)

@app.route("/")
def index():
    f = AP.getSites()
    return render_template("index.html",webpages=f)

@app.route("/remove/<webname>")
def removeWeb(webname):
    AP.removePage(webname)
    return redirect("/websites/")

@app.route("/websites/",methods = ['POST', 'GET'])
def websites():
    if request.method == 'POST':
        webname = request.form['websitename']
        AP.addPage(webname)
    f = AP.getSites()
    return render_template("websites.html",webpages=f)

@app.route("/workhours/",methods = ['POST', 'GET'])
def workhours():
    if request.method == 'POST':
        start = request.form['starthour']
        end = request.form['endhour']
        AP.setHours(start,end)
    f = AP.getSites()
    s = AP.getTimes()
    return render_template("workhours.html",webpages=f,startHour=s[0],endHour=s[1])

@app.route("/controlpanel/",methods = ['POST', 'GET'])
def controlpanel():
    if request.method == 'POST':
        code = request.form['usercode']
        print(code)
        AP.checkCode(code)
        
    if AP.allowChange == True:
        keyCode = "Key accepted! Time left:" +str(AP.timeamt-AP.count)
    else:
        keyCode = AP.getCode()
    f = AP.getSites()
    
    return render_template("controlpanel.html",webpages=f,code=keyCode)


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

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    if platform.system() == "Windows":
        if is_admin():
            watcher = threading.Thread(target=AP.block_websites).start()
            app.run(port=5002,debug=False)
        else:
    # Re-run the program with admin rights
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:

        #watcher = threading.Thread(target=block_websites).start()
        watcher = threading.Thread(target=AP.block_websites).start()
        app.run(port=5002,debug=False)

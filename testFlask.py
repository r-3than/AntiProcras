from flask import Flask, render_template ,redirect,request

app = Flask(__name__)
@app.route("/")
def index():
    f = open("blockedpages.txt").read().split("\n")
    return render_template("index.html",webpages=f)

@app.route("/remove/<webname>")
def removeWeb(webname):
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
    return redirect("/websites/")

@app.route("/websites/",methods = ['POST', 'GET'])
def websites():
    if request.method == 'POST':
        user = request.form['websitename']
        f = open("blockedpages.txt","a")
        f.write("\n"+user)
        f.close()
    f = open("blockedpages.txt").read().split("\n")
    return render_template("websites.html",webpages=f)

@app.route("/workhours/",methods = ['POST', 'GET'])
def workhours():
    if request.method == 'POST':
        start = request.form['starthour']
        end = request.form['endhour']
        f = open("state.txt","w")
        f.write(start+"|"+end+"|1")
        f.close()
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

if __name__ == '__main__':
     app.run(port=5002,debug=True)
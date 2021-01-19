from flask import Flask
from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def hello():
    return render_template("this.html")

@app.route("/test/<testname>")
def test(testname):
    f = open("./test.txt","w")
    f.write(testname)
    f.close()
    f=open("./test.txt","r").read()
    return f

if __name__ == '__main__':
     app.run(port=5002,debug=True)
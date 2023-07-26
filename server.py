from flask import Flask,request
from urllib.parse import urlparse
import os
import local
app = Flask(__name__)
app.register_blueprint(local.local,url_prefix="",host="janstraka.xyz")
app.register_blueprint(local.admin,url_prefix="/admin/",host="janstraka.xyz")


@app.before_request
def before():
    url = urlparse(request.base_url)
    hostname = url.hostname
    app.template_folder= os.getcwd() + "/apps/localhost/templates"
    app.static_folder= os.getcwd() + "/apps/localhost/static"
        



if __name__ == "__main__":
    app.run(port=40011,host="0.0.0.0")
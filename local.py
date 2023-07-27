from urllib.parse import urlparse
from flask import render_template,Blueprint,request,abort,redirect,make_response
import database
import time
import markdown
from markdown_it import MarkdownIt
import hashlib
import secrets

local = Blueprint("local",__name__)
admin = Blueprint("admin",__name__)


@local.route("/")
def start():
    return render_template("home.html")

@local.route("/social/")
def social():
    return render_template("social.html")

@local.route("/projects/")
def projects():
    return render_template("projects.html",data=database.readProjects())

@local.route("/articles/")
def articles():
    return render_template("articles.html",data=database.readArticles())

@local.route("/article/<id>/")
def article(id):
    data =  database.readArticle(id)
    if len(data) != 1:
        return abort(404)
    md = MarkdownIt()
    content = md.render(data[0][3])
    return render_template("article.html",data=data,content=content)

@local.route("/links/")
def links():
    return render_template("links.html",data=database.readLinks())


@local.route("/admin/login/")
def admin_login():
    return render_template("admin/login.html")


@local.route("/admin/action/login",methods=['GET','POST'])
def login():
    user = request.form['username']
    password = request.form['password']
    password = hashlib.sha256(password.encode()).hexdigest()
    data = database.selectUser(user,password)
    if len(data) == 1:
        token = secrets.token_hex(16)
        user = data[0][0]
        database.Auth(user,token)
        rep = make_response(redirect("/admin/"))
        rep.set_cookie('janstraka.xyz-auth',token,path="/admin/")
        return rep
    else:
        return redirect("/admin/login/")

@admin.before_request
def admin_before():
    token = request.cookies.get("janstraka.xyz-auth")
    check = database.AuthUser(token)
    if len(check) != 1:
        return redirect("/admin/login/")


@admin.route("/")
def admin_home():
    return render_template("admin/home.html")

@admin.route("/logout")
def logout():
    token = request.cookies.get("janstraka.xyz-auth")
    database.removeAuth(token)
    rep = make_response(redirect("/admin/login/"))
    rep.set_cookie('janstraka.xyz-auth',"",path="/admin/")
    return rep

@admin.route('/projects/')
def admin_projects():
    return render_template("admin/projects.html",data=database.readProjects())

@admin.route('/addproject',methods=['GET','POST'])
def admin_addproject():
    title = request.form['title']
    url = request.form['url']
    description = request.form['description']
    database.addProject(title,url,description)
    return redirect("/admin/projects")

@admin.route('/removeproject/<id>',methods=['GET','POST'])
def admin_removeproject(id):
    database.removeProject(id)
    return redirect("/admin/projects")

@admin.route("/articles/")
def admin_articles():
    return render_template("admin/articles.html",data=database.readArticles())

@admin.route("/addarticle",methods=['GET','POST'])
def admin_addarticle():
    title = request.form['title']
    description = request.form['description']
    content = request.form['content']
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    database.addArticle(title,description,content,date)
    return redirect("/admin/articles/")

@admin.route("/removearticle/<id>",methods=['GET','POST'])
def admin_removearticle(id):
    database.removeArticle(id)
    return redirect("/admin/articles/")

@admin.route("/editarticle/<id>")
def admin_editarticle(id):
    return render_template("admin/edit.html",data=database.readArticle(id))

@admin.route("/article/edit/<id>",methods=['GET','POST'])
def admin_savearticle(id):
    title = request.form['title']
    description = request.form['description']
    content = request.form['content']
    database.editArticle(id,title,description,content)
    return redirect("/admin/articles/")

@admin.route("/links/")
def admin_links():
    return render_template("admin/links.html",data=database.readLinks())

@admin.route("/addlink",methods=['GET','POST'])
def admin_addlink():
    title = request.form['title']
    link = request.form['link']
    database.addLink(title,link)
    return redirect("/admin/links/")


@admin.route("/removelink/<id>",methods=['GET','POST'])
def admin_removelink(id):
    database.removeLink(id)
    return redirect("/admin/links/")

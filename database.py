import pymysql
import sys

def get_connector():
    return pymysql.connect(host="",user="",password="",database="")


def INSERT(sql,values):
    conn = get_connector()
    cur = conn.cursor()
    cur.execute(sql,values);
    conn.commit()

def Delete(sql,values):
    conn = get_connector()
    cur = conn.cursor()
    cur.execute(sql,values)
    conn.commit()
    cur.close()
    conn.close()

def Select(sql):
    conn = get_connector()
    cur = conn.cursor()
    cur.execute(sql);
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def SelectConditional(sql,values):
    conn = get_connector()
    cur = conn.cursor()
    cur.execute(sql,values);
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def addProject(title,url,description):
    INSERT("INSERT INTO projects (title,url,description)VALUES(%s,%s,%s)",(title,url,description))

def readProjects():
    return Select("SELECT * FROM projects")

def removeProject(id):
    Delete("DELETE FROM projects where id=%s",[id])

def addArticle(title,description,content,date):
    INSERT("INSERT INTO articles(title,description,content,date)VALUES(%s, %s, %s, %s)",(title,description,content,date))

def readArticles():
    return Select("SELECT * FROM articles")

def removeArticle(id):
    Delete("DELETE FROM articles where id=%s",(id,))

def editArticle(id,title,description,content):
    conn = get_connector()
    cur = conn.cursor()
    cur.execute("UPDATE articles SET title=%s, description=%s, content=%s WHERE id=%s", (title, description, content, id))
    conn.commit()


def readArticle(id):
        conn = get_connector()
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles where id=%s",(id,));
        rows = cur.fetchall()
        return rows

def addLink(title,link):
    INSERT("INSERT INTO links (title,link)VALUES(%s,%s)",(title,link))

def readLinks():
    return Select("SELECT * FROM links")

def removeLink(id):
    Delete("DELETE FROM links where id=%s",(id,))

def selectUser(username,password):
    data = SelectConditional("SELECT id FROM users where user=%s and password=%s",(username,password))
    return data

def Auth(id,token):
    INSERT("INSERT INTO auth(user_id,token)VALUES(%s,%s)",(id,token))

def AuthUser(token):
    return SelectConditional("SELECT * FROM auth where token=%s",[token])

def removeAuth(token):
    Delete("DELETE FROM auth where token=%s",[token])
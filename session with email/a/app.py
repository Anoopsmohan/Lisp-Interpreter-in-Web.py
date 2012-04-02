import web,sqlite3,hashlib,base64
from web import form
import lisp
import lispio
from lisp import *
Alist=[]

web.config.debug = False

urls = ('/', 'home',
'/signin.html','signin',
'/signup.html','signup',
'/tutorial','tutorial',
'/register_success', 'regsuccess',
'/signin_fail','signfail',
'/home.html','home',
'/signin_error1','signerror',
'/signin_after.html','signafter',
'/about_us.html','aboutus',
'/contact_us.html','contact',
'/examples.html','examples',
'/feed_back.html','feedback',
'/about.html','about',
'/signout','signout')

app = web.application(urls, globals(),True)
store = web.session.DiskStore('sessions')

if web.config.get('_session') is None:
        session = web.session.Session(app,store,initializer={'login': 0,'privilege': 0,'user':'anonymous','loggedin':False})
        web.config._session = session
else:
        session = web.config._session
render = web.template.render('templates/',globals={'context': session})

web.config.smtp_server = 'smtp.gmail.com'
web.config.smtp_port = 587
web.config.smtp_username = 'username'
web.config.smtp_password = 'password'
web.config.smtp_starttls = True

my_form = web.form.Form(
                web.form.Textarea('', class_='text_area3', id='textfield', cols="40", rows="6")
                )

class home:
    def GET(self):
	conn = sqlite3.connect('anoop.db')
        curs = conn.cursor()
	check = curs.execute('''select name,message from comments''')
        count = check.fetchall()
	return render.home(count)

    def POST(self):
	cmts =  web.input()
        conn = sqlite3.connect('anoop.db')
        curs = conn.cursor()
        curs.execute('''insert into comments values(?,?,?)''',(cmts.name, cmts.email, cmts.message))
        conn.commit()
        raise web.redirect('/home.html')


class signout:
    def GET(self):
        session.kill()
	conn = sqlite3.connect('anoop.db')
        curs = conn.cursor()
	check = curs.execute('''select name,message from comments''')
        count = check.fetchall()
	return render.home(count)

class signin:
    def GET(self):
	return render.signin()

    def POST(self):
        fi =  web.input()
        conn = sqlite3.connect('anoop.db')
        curs = conn.cursor()
        check = curs.execute('''select * from register where email=? and password=? ''',(fi.email, fi.password))
        count = check.fetchall()
        if len(count)!=0: 
            session.loggedin = True
            session.username = fi.email
            raise web.redirect('/tutorial')
        else:
            raise web.redirect('/signin_error1')
	session.username=context.username

class signfail:
    def GET(self):
	return render.signin_fail()

    def POST(self):
        fi =  web.input()
        conn = sqlite3.connect('anoop.db')
        curs = conn.cursor()
        check = curs.execute('''select * from register where email=? and password=? ''',(fi.email, fi.password))
        count = check.fetchall()
        if len(count)!=0: 
            session.loggedin = True
            session.username = fi.email
            raise web.redirect('/tutorial')
        else:
            raise web.redirect('/signin_fail')

class signerror:
    def GET(self):
	return render.signin_error1()

    def POST(self):
        fi =  web.input()
        conn = sqlite3.connect('anoop.db')
        curs = conn.cursor()
        check = curs.execute('''select * from register where email=? and password=? ''',(fi.email, fi.password))
        count = check.fetchall()
        if len(count)!=0: 
            session.loggedin = True
            session.username = fi.email
            raise web.redirect('/tutorial')
        else:

            raise web.redirect('/signin_fail')



class signup:
    def GET(self):
	return render.signup()

    def POST(self):
        fi =  web.input()
        conn = sqlite3.connect('anoop.db')
        curs = conn.cursor()
	#try:
	curs.execute('''insert into register values(?,?,?,?,?,?,?,?)''',(fi.username, fi.password, fi.email, fi.firstname, fi.lastname, fi.age, fi.gender, fi.country))
        conn.commit()
	session.loggedin = True
        session.email = fi.email
        session.user = fi.firstname
        subject = "Thanks for joining Git Wiki"
        message = ("Dear %s,\n\n\t Thanks for joining our site.\n\t Your Account Details : \n\n\t\t\t username = %s\n\t\t\t password = %s\n\n\t Keep updated with regular articles.\n\n\t Thank you.\n\t Admin.\n\t Git Wiki\n\t\t\t\tBlog : http://Anoopsmohan.blogspot.com/" % (fi.firstname,fi.email,fi.password))
        web.sendmail('anoopmhn2008@gmail.com', fi.email, subject, message)
        #return render.static_data(session.user,"Sign Out","Successfully Registered","Success")
        #except sqlite3.IntegrityError:
        #return render.signup("Guest","Sign In","Email id already registered. Try another mail id",fi.firstname,fi.lastname,fi.dd,fi.mm,fi.yyyy)

        raise web.redirect('/register_success')

class regsuccess:
    def GET(self):
	return render.register_success()


class signafter:
    def GET(self):
	return render.signin_after()

    def POST(self):
        fi =  web.input()
        conn = sqlite3.connect('anoop.db')
        curs = conn.cursor()
        check = curs.execute('''select * from register where email=? and password=? ''',(fi.email, fi.password))
        count = check.fetchall()
        if len(count)!=0: 
            session.loggedin = True
            session.username = fi.email
            raise web.redirect('/tutorial')
        else:
            raise web.redirect('/signin_fail')
	

class tutorial:
    def GET(self):
        form = my_form()
        return render.tutorial(form, "Result")
        
    def POST(self):
	Alist=lisp.Alist
	global data1
	
        form = my_form()
        form.validates()
	#f = open('test.txt','w')
        data1 = form.value['textfield']
	
	#f.write(str(data1))
	try:
	    s=lispio.getSexp()
	except:
	    return "Invalid Input"
        #f.write(str(s))
	#f.close()
	try:
	    list1=lispio.putSexp(eval(s,Alist))
	#return str(list1)
	
	    return str(list1)
	except:
	    return "???"


class aboutus:
    def GET(self):
	return render.about_us()
    def POST(self):
	cmts =  web.input()
        conn = sqlite3.connect('anoop.db')
        curs = conn.cursor()
        curs.execute('''insert into comments values(?,?,?)''',(cmts.name, cmts.email, cmts.message))
        conn.commit()
        raise web.redirect('/about_us.html')



class contact:
    def GET(self):
	
	return render.contact_us()
    def POST(self):
	cmts =  web.input()
        conn = sqlite3.connect('anoop.db')
        curs = conn.cursor()
        curs.execute('''insert into comments values(?,?,?)''',(cmts.name, cmts.email, cmts.message))
        conn.commit()
        raise web.redirect('/contact_us.html')
 
class feedback:
    def GET(self):
	conn = sqlite3.connect('anoop.db')
        curs = conn.cursor()
	check = curs.execute('''select name,message from comments''')
        count = check.fetchall()
	return render.feed_back(count)

    def POST(self):
	cmts =  web.input()
        conn = sqlite3.connect('anoop.db')
        curs = conn.cursor()
        curs.execute('''insert into comments values(?,?,?)''',(cmts.name, cmts.email, cmts.message))
        conn.commit()
        raise web.redirect('/feed_back.html')



class about:
    def GET(self):
        return render.about()

class examples:
    def GET(self):
	return render.examples()


if __name__ == '__main__':
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0",8080))
    app.run()



#####################################################################
### Assignment skeleton
### You can alter the below code to make your own dynamic website.
### The landing page for assignment 3 should be at /
#####################################################################

from bottle import route, run, default_app, debug, static_file, template, request, TEMPLATES
from hashlib import sha256
from datetime import datetime
from pytz import timezone

# BORROWED CODE
# See the original:
# https://bitbucket.org/damienjadeduff/hashing_example/raw/master/hash_password.py

def create_hash(password):
	pw_bytestring = password.encode()
	return sha256(pw_bytestring).hexdigest()

# BORROWED CODE END
	
'''
def htmlify(title,text):
	page = """
		<!doctype html>
		<html lang="en">
			<head>
				<meta charset="utf-8" />
				<title>%s</title>
			</head>
			<body>
			%s
			</body>
		</html>

	""" % (title,text)
	return page
'''

@route("/<page_name>")
def tpl_strip(page_name):
	return static_file(page_name + '.tpl', root='.')
	
@route("/shows")
def add_comment_form():
	comment_box_html =  """
						<form class="comment-box" action="/" method="POST">
							<div class="comment-box-password">
								<label for="password">Password:</label>
								<input type="password" name="password" id="password" placeholder="The password is..." required>
							</div>
							<br>
							<div class="comment-box-nickname">
							<label for="nickname">Nickname:</label>
							<input type="text" name="nickname" id="nickname" placeholder="Call me..." required>
							</div>
							<br>
							<div class="comment-box-visibility">
							<input type="radio" name="visibility" value="visible" checked="checked"> Show my nickname<br>
							<input type="radio" name="visibility" value="anon"> Don't show my nickname<br>
							</div>
							<br>
							<div class="comment-box-comment">
								<label for="comment">Your comment:</label>
								<br>
								<textarea name="comment" id="comment" placeholder="The thing is..." required></textarea>
							</div>
							<input type="submit" name="send_button" value="Send"/>
						</form>
						<br>
						"""
	comment_box_css =   """
						<style type="text/css">
						.comment-box {
							margin: 100px 0 20px 0;
							padding: 60px 0;
							background-color: rgba(165, 64, 64, 1);
							border-radius: 15px;

						}

						.comment-box-password, .comment-box-nickname {
							display: flex;
							text-align: center;
							justify-content: center;
							font-size: 2em;
						}

						.comment-box-visibility {
							text-align: center;
							justify-content: center;
						}
						
						.comment-box-comment {
							text-align: center;
							font-size: 2em;
						}

						.comment-box [id="password"], .comment-box [id="nickname"] {
							text-align: center;
							border-radius: 5px;
							border: 1px solid grey;
							margin: 0 25px;
							font-size: 0.5em;
						}
						
						.comment-box [name="visibility"] {
							text-align: center;
							font-size: 1em;
						}

						.comment-box [id="comment"] {
							border-radius: 5px;
							border: 1px solid grey;
							width: 50%;
							height: 180px;
							font-family: 'Lato', sans-serif;
							font-size: 0.5em;
							padding: 10px 5px;
						}

						.comment-box [name="send_button"] {
							width: 100px;
							height: 60px;
							font-size: 0.6em;
							margin: auto;
							display: block;
							font-family: 'Noto Serif', serif;
							color: rgba(178, 178, 181, 1);
							text-transform: uppercase;
							border-radius: 10px 0;
							box-sizing: border-box;
							-moz-box-sizing: border-box;
							-webkit-box-sizing: border-box;
							background: linear-gradient(rgba(100, 100, 100, 1) 50%, rgba(71, 71, 71, 1) 50%);
							border: 2px solid rgba(71, 71, 71, 1);
						}
						.comment-box [name="send_button"]:hover {
							background: rgba(71, 71, 71, 1);
						}
						
						#ul_comments {
							text-align: center;
							font-size: 1em;
						}
						
						#ul_comments ul {
							list-style: none;
						}
						
						#ul_comments li {
							margin-bottom: 30px;
						}
						</style>
						"""
	comment_list = []					
	file = open("comments.txt", "r")
	comment_list += file.readlines()
	comment_list.reverse()
	html_comments = "<ul>"
	for line in comment_list:
		html_comments += ("\n<li>" + line + "</li>")
	
	html_comments += "\n</ul>"
	file.close()
						
	info = {'commentbox': comment_box_html,
			'commentboxstyle': comment_box_css,
			'commentlist': html_comments}

	new_html = template("shows", info) 
	return new_html
	
@route("/", method='POST')
def send_comment():
	password_hash = "4f1a9e1058dd06089804da225f66f433859138e42c204856b2903fd8181dfea6"
	visibility = request.forms.get("visibility")
	nickname = request.forms.get("nickname") if visibility == "visible" else "Anonymous"
	comment = request.forms.get("comment")
	pass_input = request.forms.get('password')
	hash_input = create_hash(pass_input)

	if (hash_input == password_hash):	
		time = datetime.now(timezone('Europe/Istanbul'))
		time_string = datetime.strftime(time, '%d/%m/%Y %H:%M')
		
		file = open("comments.txt", "a")
		file.write(nickname + "<br>" + time_string + "<br>" + comment + "\n") 
		file.close()
		
		response_html = """
						<!DOCTYPE html>
						<html lang ="en">
							<head>
								<meta charset="utf-8"> 
								<title>Primetime</title>
								<link rel="stylesheet" href="./css/stylesheet.css" />
								<link href="https://fonts.googleapis.com/css?family=Lato:400,400i,700" rel="stylesheet">
								<link href="https://fonts.googleapis.com/css?family=Noto+Serif:700" rel="stylesheet">
								<link rel="shortcut icon" type="image/png" href="./img/favicon.png">
								<style>
									.response{
										text-align: center;
									}
								</style>
							</head>
							<body>
								<header>
									<nav>
										<ul class="left-nav">
											<li><a href="./">Home</a></li>
											<li><a href="./about">About</a></li>
										</ul>
										 <img src="./img/logo.svg" alt="Primetime" width="240" height="80" class="center-logo">
										<ul class="right-nav">
											<li><a href="./shows">Shows</a></li>
										</ul>
									</nav>
								</header>
								<main>
								<div class="content">
									<div class="content-title">
										<h2>Successful!</h2>
									</div>
									<div class="sub-content">
										<div class ="response">
										<img src="./img/pass_success.png" alt="Your comment has been submitted!" width="350">
										<p>Your comment has been submitted!</p>
										<a href="./shows#ul_comments">Let me see!</a>
										</div>
									</div>
								</div>
								</main>
								<footer class="page-footer">
									<p>Made by Erkin Sahin with love and procrastination.</p>
									<a href="https://www.instagram.com/sahnerkin" target="_blank">Let's keep in touch!</a>
								</footer>
							</body>
						</html>
						"""
	else:
		response_html = """
						<!DOCTYPE html>
						<html lang ="en">
							<head>
								<meta charset="utf-8"> 
								<title>Primetime</title>
								<link rel="stylesheet" href="./css/stylesheet.css" />
								<link href="https://fonts.googleapis.com/css?family=Lato:400,400i,700" rel="stylesheet">
								<link href="https://fonts.googleapis.com/css?family=Noto+Serif:700" rel="stylesheet">
								<link rel="shortcut icon" type="image/png" href="./img/favicon.png">
								<style>
									.response{
										text-align: center;
									}
								</style>
							</head>
							<body>
								<header>
									<nav>
										<ul class="left-nav">
											<li><a href="./">Home</a></li>
											<li><a href="./about">About</a></li>
										</ul>
										 <img src="./img/logo.svg" alt="Primetime" width="240" height="80" class="center-logo">
										<ul class="right-nav">
											<li><a href="./shows">Shows</a></li>
										</ul>
									</nav>
								</header>
								<main>
								<div class="content">
									<div class="content-title">
										<h2>Something went wrong!</h2>
									</div>
									<div class="sub-content">
										<div class ="response">
										<img src="./img/pass_fail.png" alt="Your authentication has failed." width="350">
										<p>Your authentication has failed. Perhaps you've mistyped your password.</p>
										<a href="./shows#add_comments">Try again</a>
										</div>
									</div>
								</div>
								</main>
								<footer class="page-footer">
									<p>Made by Erkin Sahin with love and procrastination.</p>
									<a href="https://www.instagram.com/sahnerkin" target="_blank">Let's keep in touch!</a>
								</footer>
							</body>
							
						</html>
						"""
	return response_html
	

# FETCHING OF STATIC FILES (NECESSARY FOR RUNNING ON HEROKU):
	
@route('/css/<stylesheet:re:.*\.css>')
def fetch_stylesheet(stylesheet):
	return static_file(stylesheet, root='./css', mimetype='text/css')	
	
@route('/img/<png_file:re:.*\.png>')
def fetch_png(png_file):
	return static_file(png_file, root='./img', mimetype='image/png')
	
@route('/img/<jpg_file:re:.*\.jpg>')
def fetch_jpg(jpg_file):
	return static_file(jpg_file, root='./img', mimetype='image/jpeg')
	
@route('/font/<woff_file:re:.*\.woff>')
def fetch_woff(woff_file):
	return static_file(woff_file, root='./font', mimetype='application/x-font-woff')

@route('/font/<woff2_file:re:.*\.woff>')
def fetch_woff(woff2_file):
	return static_file(woff2_file, root='./font', mimetype='application/x-font-woff')

@route('/img/<svg_file:re:.*\.svg>')
def fetch_woff(svg_file):
	return static_file(svg_file, root='./img', mimetype='image/svg+xml')

@route('/')
def index():
	return static_file('index.tpl', root='./')


#####################################################################
### Don't alter the below code.
### It allows this website to be hosted on Heroku
### OR run on your computer.
#####################################################################

# This line makes bottle give nicer error messages
debug(False)
# This line is necessary for running on Heroku
app = default_app()
# The below code is necessary for running this bottle app standalone on your computer.
if __name__ == "__main__":
  run()

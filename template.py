def header ():
	return "Content-Type: text/html\r\n"

def head (stylesheets):
	returnstring = '''
	<!DOCTYPE html>
	<html>
	<head>
		<meta charSet="utf8"/>'''
	for sheet in stylesheets:
		returnstring = returnstring + '<link rel="stylesheet" type="text/css" href="styles/' + sheet + '.css">'
	returnstring = returnstring + '''</head>
	<body>
		<div class="wsnavbar">
			<div class="wstitle">webshrink</div>
			<form class="wsurlform">
				<input type="text" name="url" placeholder="https://example.com" class="wsurlbox">
				<input type="submit" class="wssubmit" value="Shrink">
			</form>
			<a href="settings.py"><div class="wssettings">Settings</div></a>
		</div>
		<div class="wswrapper">
	'''
	return returnstring

def foot ():
	return '''
	</div>
	</body>
	</html>
	'''

def info ():
	return '''
	<p class="infoblurb">Use webshrink to browse the internet with text only and avoid data charges. Enter a url and click "Shrink" to begin!</p>
	'''
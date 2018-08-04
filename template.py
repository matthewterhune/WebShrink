def header ():
	return "Content-Type: text/html\r\n"

def head (stylesheets):
	returnstring = '''
	<!DOCTYPE html>
	<html>
	<head>
		<meta charSet="utf8"/>'''
	for sheet in stylesheets:
		returnstring = returnstring + '<link rel="stylesheet" type="text/css" href="' + sheet + '.css">'
	returnstring = returnstring + '''</head>
	<body>
		<div class="wsnavbar">
			<div class="wstitle">webshrink</div>
			<form class="wsurlform">
				<input type="text" name="url" placeholder="https://example.com" class="wsurlbox">
				<input type="submit" class="wssubmit" value="Shrink">
			</form>
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


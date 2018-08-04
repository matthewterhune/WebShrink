header = "Content-Type: text/html\r\n"

head = '''
<!DOCTYPE html>
<html>
<head>
	<meta charSet="utf8"/>
	<link rel="stylesheet" type="text/css" href="default.css">
</head>
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

foot = '''
</div>
</body>
</html>
'''

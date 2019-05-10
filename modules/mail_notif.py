import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

port = 465  # SSL

# Secure SSL Context
context = ssl.create_default_context()

def createMessage(config):

	"""
	<div style="width: 100%; display: table;">
		<div style="display: table-row">
			<div style="width: 400px; display: table-cell;">
			<table>
			  <tr>
				<th style="font-weight: 800">CPU/Memory parameters</th>
				<th style="font-weight: bolder">Minimum</th>
				<th style="font-weight: bolder">Maximum</th>
			  </tr>
			  <tr>
				<td>CPU usage</td>
				<td>{} %</td>
				<td>{} %</td>
			  </tr>
			  <tr>
				<td>Virtual memory usage</td>
				<td>{} MB</td>
				<td>{} MB</td>
			  </tr>
			</table>
		  </div>
		<div style="display: table-cell;">
		  <table>
			<tr>
			  <th style="font-weight: 800">Time Intervals</th>
			  <th style="font-weight: bolder">Minimum</th>
			  <th style="font-weight: bolder">Maximum</th>
			</tr>
			<tr>
			  <td>CPU usage</td>
			  <td>10 %</td>
			  <td>90 %</td>
			</tr>
			<tr>
			  <td>Virtual memory usage</td>
			  <td>1000 MB</td>
			  <td>9000 MB</td>
			</tr>
		  </table>
		</div>
	</div>
	"""

	html = """
	<style>
	.floatedTable {{
  		float:left;
	}}
	.inlineTable {{
  		display: inline-block;
	}}
	h1 {{
		font-size: 50px;
	}}
	
	table {{
		font-family: arial, sans-serif;
		border-collapse: collapse;
	}}
	
	td, th {{
		border: 1px solid #dddddd;
		text-align: left;
		padding: 8px;
	}}
	</style>
	<h1 style="text-align: center;"><strong>Periodic Report</strong></h1>
	<p>&nbsp;</p>
	<h2>Configurations:</h2>
	<table class="inlineTable">
		<thead>
			<tr>
				<th style="font-weight: 800">CPU/Memory configuration</th>
				<th style="font-weight: bolder">Minimum</th>
				<th style="font-weight: bolder">Maximum</th>
			</tr>
		</thead>
			<tbody>
				<tr>
				<td>CPU usage</td>
				<td>{} %</td>
				<td>{} %</td>
			</tr>
			<tr>
				<td>Virtual memory usage</td>
				<td>{} MB</td>
				<td>{} MB</td>
			</tr>
		</tbody>
	</table>
	<table class="inlineTable">
		<tr>
			<th rowspan="2" style="font-weight: 800" width="10" height="90">Time intervals</th>
			<th width=70>Autopsy process</th>
			<th width=10>Periodic report</th>
		</tr>
		<tr>
			<td width=140>Autopsy processes are monitored every {} seconds</td>
			<td width=330>The periodic report is sent to <u>{}</u> every {} seconds</td>
		</tr>
	</table>
	<p>&nbsp;</p>
	<h2><strong>Statistics:</strong></h2>
	<p><strong>CPU:</strong></p>
	<img src="cid:cpu_usage" alt="" style="float: left; width: 45%; margin-right: 1%; margin-bottom: 0.5em;"/>
	<img src="cid:cpu_cores" alt="" style="float: left; width: 45%; margin-right: 1%; margin-bottom: 0.5em;"/>
	<p style="clear: both;">
	<img src="cid:cpu_threads" alt="" style="float: left; width: 45%; margin-right: 1%; margin-bottom: 0.5em;"/>
	<img src="cid:cpu_time" alt="" style="float: left; width: 45%; margin-right: 1%; margin-bottom: 0.5em;"/>
	<p style="clear: both;">
	<p>&nbsp;</p>
	<p><strong>IO:</strong></p>
	<!--<img src="cid:io" alt="" style="float: left; width: 45%; margin-right: 1%; margin-bottom: 0.5em;"/>-->
	<img src="cid:io" alt="" style="float: left; width: 45%; margin-right: 1%; margin-bottom: 0.5em;"/>
	<p style="clear: both;">
	<p>&nbsp;</p>
	<p><strong>Memory:</strong></p>
	<img src="cid:memory" alt="" style="float: left; width: 45%; margin-right: 1%; margin-bottom: 0.5em;"/>
	<p style="clear: both;">
	<p>&nbsp;</p>
	<p>&nbsp;</p>
	<p>&nbsp;</p>
	<p>&nbsp;</p>
	<h2><strong>Program Execution:</strong></h2>
	<p><img src="cid:status" alt="" width="1920" height="1080" /></p>
	<p>&nbsp;</p>""".format(config["CPU USAGE"]["min"], config["CPU USAGE"]["max"], config["MEMORY"]["min"], config["MEMORY"]["max"], config["TIME INTERVAL"]["process"], config["NOTIFY"]["receiver_email"], config["TIME INTERVAL"]["report"])


	# html = """<h1 style="text-align: center;"><strong>Periodic Report</strong></h1>
	# <p>&nbsp;</p>
	# <h2><strong>Parameters:</strong></h2>
	# <ul>
	# <li><strong>CPU Usage</strong>:
	# <ul>
	# <li>Minimum: {}%</li>
	# <li>Maximum: {}%</li>
	# </ul>
	# </li>
	# <li><strong>Virtual Memory Usage</strong>:
	# <ul>
	# <li>Minimum: {}MB</li>
	# <li>Maximum: {}MB</li>
	# </ul>
	# </li>
	# </ul>
	# <p>&nbsp;</p>
	# <h2><strong>Statistics:</strong></h2>
	# <p><strong>CPU:</strong></p>
	# <p><strong><img src="cid:cpu" alt="" width="836" height="526" /></strong></p>
	# <p>&nbsp;</p>
	# <p><strong>IO:</strong></p>
	# <p><strong><img src="cid:io" alt="" width="836" height="526" /></strong></p>
	# <p>&nbsp;</p>
	# <p><strong>Memory:</strong></p>
	# <p><strong><img src="cid:memory" alt="" width="836" height="526" /></strong></p>
	# <p>&nbsp;</p>
	# <p>&nbsp;</p>
	# <p>&nbsp;</p>
	# <p>&nbsp;</p>
	# <h2><strong>Program Execution:</strong></h2>
	# <p><img src="cid:status" alt="" width="1920" height="1080" /></p>
	# <p>&nbsp;</p>""".format(config["CPU USAGE"]["min"], config["CPU USAGE"]["max"], config["MEMORY"]["min"], config["MEMORY"]["max"])

	message = MIMEMultipart("related")
	message["Subject"] = "Periodic Report"
	message["From"] = "noreply@MonAutopsy.pt"
	msgAlternative = MIMEMultipart('alternative')
	message.attach(msgAlternative)

	part1 = MIMEText(html, "html")
	msgAlternative.attach(part1)

	fp = open("cpu_usage.png", "rb")
	msgImage = MIMEImage(fp.read())
	msgImage.add_header('Content-ID', '<cpu_usage>')
	message.attach(msgImage)
	fp.close()

	fp = open("cpu_cores.png", "rb")
	msgImage = MIMEImage(fp.read())
	msgImage.add_header('Content-ID', '<cpu_cores>')
	message.attach(msgImage)
	fp.close()

	fp = open("cpu_threads.png", "rb")
	msgImage = MIMEImage(fp.read())
	msgImage.add_header('Content-ID', '<cpu_threads>')
	message.attach(msgImage)
	fp.close()

	fp = open("cpu_time.png", "rb")
	msgImage = MIMEImage(fp.read())
	msgImage.add_header('Content-ID', '<cpu_time>')
	message.attach(msgImage)
	fp.close()

	fp = open("io.png", "rb")
	msgImage = MIMEImage(fp.read())
	msgImage.add_header('Content-ID', '<io>')
	message.attach(msgImage)
	fp.close()

	fp = open("memory_usage.png", "rb")
	msgImage = MIMEImage(fp.read())
	msgImage.add_header('Content-ID', '<memory>')
	message.attach(msgImage)
	fp.close()

	#Change when screenshot.py works
	fp = open("autopsy.png", "rb")
	msgImage = MIMEImage(fp.read())
	msgImage.add_header('Content-ID', '<status>')
	message.attach(msgImage)
	fp.close()

	return message

def send_notif(config, SMTPServer, senderEmail, receiverEmail, password):
	message = createMessage(config)
	with smtplib.SMTP_SSL(SMTPServer, port, context=context) as server:
		server.login(senderEmail, password)
		server.sendmail(senderEmail, receiverEmail, message.as_string())

def check_authentication(SMTPServer, senderEmail, password):
	with smtplib.SMTP_SSL(SMTPServer, port, context=context) as server:
		try:
			server.login(senderEmail, password)
			return True
		except smtplib.SMTPException as e:
			print(e)
			return False
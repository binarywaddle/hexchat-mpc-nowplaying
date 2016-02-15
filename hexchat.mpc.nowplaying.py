# Inspired by https://github.com/mpc-hc/snippets
# Inspired by https://github.com/derekxwu/hexchat.np.mpc-hc/
# This script should work with any Media Player Classic alternative that has a web interface, although I don't guarantee the formatting.
# Author Sengoku Nadeko
# Date 14/02/16

import hexchat
import requests
from bs4 import BeautifulSoup
import re

__module_name__ = 'MPC Now Playing'
__module_version__ = '0.7'
__module_description__ = 'MPC-BE/HC Now Playing script'


def now_playing(word, word_eol, userdata):
	try:
	# URL for MPC web interface. Check under Options -> Web Interface, listen on port and allow localhost only.
		url = 'http://127.0.0.1:13579/info.html'
	
	# Request the URL
		r = requests.get(url)

	# Get the body of the page
		html_content = r.text
	
	# Convert the html content into a beautiful soup object
		soup = BeautifulSoup(html_content, "html5lib")

	# If no web interface then MPC isn't running
	except:
		hexchat.prnt('Nothing open in MPC')
		return
		
	# Get the info from the page to parse with regex
	nowplaying = soup.p.string
	
	# Take the text found on the page and run it through regex to grab the info	
	line = re.search('(MPC.*?)\s(.*?)\s•\s(.*?)\s•\s(.*?)\s.?(.*?(GB|MB))', nowplaying)
	if len(word) > 1 and (word[1] == 'v' or word[1] == 'full'):
		hexchat.command('SAY Now Playing in {1} : {3} @ {4} [{5}]'.format(line.group(0), line.group(1), line.group(2), line.group(3), line.group(4), line.group(5)))
	else:
		hexchat.command('SAY Now Playing in {1} : {3} '.format(line.group(0), line.group(1), line.group(2), line.group(3), line.group(4), line.group(5)))
	return hexchat.EAT_ALL
	
def unload_callback(userdata):
	hexchat.prnt('Now Playing script unloaded.')


# Hexchat hooks - Command to set in hexchat
hexchat.hook_command('np', now_playing, help='"/np" to display currently playing MPC media, "/np full" to show full info.')
hexchat.hook_unload(unload_callback)
hexchat.prnt('hexchat.mpc.nowplaying loaded')
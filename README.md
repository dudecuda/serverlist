Minetest server list - Ping Removed Fork
========================================

At this very moment, this is simply a placeholder until I can upload a few of the changes I made work. 
Essentially removes a few features, primarily ping, that become redundant and interfere if using as an internal operation (i.e., running a serverlist server to list worlds running on the same machine it's running on). 

The default serverlist sends a ping back after recieving an update from a Minetest server, which then feeds the lag time column on the webpage, as well as fed to clients using the serverlist. I have successfuly removed this response from the serverlist, as there is no need for a machine to ping itself for a network response time. 

Todo:
1. Update the changes from what I successfully have working in this setup (other computer at the moment).
2. Remove a few parameters that refer to lag time from this ping on the actual list webpage. In the setup I'm trying to produce, all worlds would be on the same machine, and thus would have the sam ping. 
3. I might integrate a way to ping to some custom server address to just get some idea of response time to list. But in the setup that I'm aiming for, this would be more something to list at the top of the page as applying to all servers, rather than per server basis. 

The rest of the readme is as per the master branch at https://github.com/minetest/serverlist

Setting up the webpage
----------------------

You will have to install node.js, doT.js and their dependencies to compile
the server list webpage template.

First install node.js, e.g.:

	# apt-get install nodejs
	# # OR:
	# pacman -S nodejs

Then install doT.js and its dependencies:

	$ npm install dot commander mkdirp

And finally compile the template:

	$ cd static
	$ ../node_modules/dot/bin/dot-packer -s .

You can now serve the webpage by copying the files in static/ to your web root, or by [starting the server list](#setting-up-the-server).


Embedding the server list in a page
-----------------------------------

	<head>
		...
		<script>
			var master = {
				root: 'http://servers.minetest.net/',
				limit: 10,
				clients_min: 1,
				no_flags: 1,
				no_ping: 1,
				no_uptime: 1
			};
		</script>
		...
	</head>
	<body>
		...
		<div id="server_list"></div>
		...
	</body>
	<script src="list.js"></script>


Setting up the server
---------------------

  1. Install Python 3 and pip:

	pacman -S python python-pip
	# OR:
	apt-get install python3 python3-pip

  2. Install required Python packages:

	# You might have to use pip3 if your system defaults to Python 2
	pip install -r requirements.txt

  3. If using in production, install uwsgi and it's python plugin:

	pacman -S uwsgi uwsgi-plugin-python
	# OR:
	apt-get install uwsgi uwsgi-plugin-python
	# OR:
	pip install uwsgi

  4. Configure the server by adding options to `config.py`.
       See `config-example.py` for defaults.

  5. Start the server:

	$ ./server.py
	$ # Or for production:
	$ uwsgi -s /tmp/minetest-master.sock --plugin python -w server:app --enable-threads
	$ # Then configure according to http://flask.pocoo.org/docs/deploying/uwsgi/

  7. (optional) Configure the proxy server, if any.  You should make the server
	load static files directly from the static directory.  Also, `/list`
	should be served from `list.json`.  Example for nginx:

	root /path/to/server/static;
	rewrite ^/list$ /list.json;
	try_files $uri @uwsgi;
	location @uwsgi {
		uwsgi_pass ...;
	}

Setting up the server (Apache version)
---------------------

If you wish to use Apache to host the server list, do steps 1-2, 4, above. Additionally install/enable mod_wsgi and an Apache site config like the following:

		# This config assumes you have the server list at DocumentRoot.
		# Visitors to the server list in this config would visit http://local.server/ and
		# apache would serve up the output from server.py. Static resources would be served
		# from http://local.server/static.

		# Where are the minetest-server files located?
		DocumentRoot /var/games/minetest/serverlist

		# Serve up server.py at the root of the URL.
		WSGIScriptAlias / /var/games/minetest/serverlist/server.py

		# The name of the function that we call when we invoke server.py
		WSGICallableObject app

		# These options are necessary to enable Daemon mode. Without this, you'll have strange behavior
		# with servers dropping off your list! You can tweak threads as needed. See mod_wsgi documentation.
		WSGIProcessGroup minetest-serverlist
		WSGIDaemonProcess minetest-serverlist threads=2


		<Directory /var/games/minetest/serverlist>
			Require all granted
		</Directory>

	</VirtualHost>

License
-------

The Minetest server list code is licensed under the GNU Lesser General Public
License version 2.1 or later (LGPLv2.1+).  A LICENSE.txt file should have been
supplied with your copy of this software containing a copy of the license.

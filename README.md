What is CoD4 CPSP?
------------------
CoD4 CPSP is a small script designed to protect your CoD4 server from those retards who think flooding your server with fake players is funny.

What do I need to run it?
-------------------------
You need root access to your server as well as a Python interpreter. Optional but you should use tmux to run the script in, you can use screen but I do prefer tmux. You may edit the ban line to your liking but it's configured for csf.

How does this shit work?
------------------------
The script works by polling the server for a "status" every n amount of seconds, it then counts how many players are in CNCT status and firewalls the IP if the count of concurrent connecitons is above n amount.

Important Notes
---------------
If your RCON is floodable, then this little workaround will NOT work as most fake player spam bots come with an RCON flooder.
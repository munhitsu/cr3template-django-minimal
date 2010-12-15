cr3template-minimal-django
=======================================
Minimal template for cr3studio projects


Project start
-------------
- Download template
- initialize git local repo:
	git init
- edit project name in buildout.cfg
- execute make
- alter settings.py


fab goodies (connecting with remote server)
-------------------------------------------
- edit fabfile.py (username/server)
- ./bin/fab prod ssh_register (if you have private dsa key in default location)
- initialize master repository:
	./bin/fab prod init_master_repo
- connect local repo:
	./bin/fab prod connect_local
- create remote site (app instance)
	./bin/fab prod init_master_site
- initial push
	git add . -m "Initial"
	git push origin master
- register deployment key to cr3components git repo
	ssh server
	ssh-keygen -t dsa
	cat $HOME/.ssh/id_dsa.pub
register it using: https://github.com/munhitsu/cr3components/admin
- start app:
	ssh server
	cd django_site
	make
	/cr3studio/bin/restart-app-django


Other steps
-----------
- precondition is to have libjpeg installed on dev host (in case of cms usage)




urls.py
-------
take from cr3components app (it's in parts dir)

settings.py
-----------
take from cr3components app (it's in parts dir)


----
TODO
----
make fabfile.py project independent (remote username is in there)
how to embed some settings goodies

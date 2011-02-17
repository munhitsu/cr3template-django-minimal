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
- edit fabfile.py in case default username=project_name and servers are to be changed
- register your ssh key on all servers
	./bin/fab -R prod ssh_register
	./bin/fab -R dev ssh_register
- initialize master repositories:
	./bin/fab -R prod init_remote_repo
	./bin/fab -R dev init_remote_repo
- connect local repo to prod:
	./bin/fab -R prod configure_remote_branch:prod,master
	./bin/fab -R dev configure_remote_branch
- let's create master branch
	git add .
	git commit -m "Initial"
- now we can create dev branch
	git branch dev
	git checkout dev
- ready to push
	git push dev dev
	git push prod master
- create remote site (app instance)
	./bin/fab -R prod init_remote_site:master
	./bin/fab -R dev init_remote_site
- register deployment key to cr3components git repo
	./bin/fab -R prod ssh_remote_keygen
	./bin/fab -R dev ssh_remote_keygen
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
make fabfile.py project independent (username=project_name, servernames)
how to embed some settings goodies
project name and server names are not DRY

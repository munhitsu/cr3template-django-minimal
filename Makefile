.DEFAULT_GOAL = development
.PHONY = development clean
ARCHFLAGS = "-arch i386 -arch x86_64"


bootstrap.py :
	wget http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py
	patch bootstrap.py < patches/bootstrap.py.patch

bin/buildout : bootstrap.py
	python bootstrap.py

development : bin/buildout
	env ARCHFLAGS=${ARCHFLAGS} bin/buildout

clean :
	rm -rf bin develop-eggs eggs parts .installed.cfg downloads bootstrap.py *.db
	find . -name "*~" -exec rm {} \;
	find . -name "DEADJOE" -exec rm {} \;
	find . -name "*.pyc" -exec rm {} \;

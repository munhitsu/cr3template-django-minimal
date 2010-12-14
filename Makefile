.DEFAULT_GOAL = development
.PHONY = development clean

bootstrap.py :
	wget http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py
	patch bootstrap.py < patches/bootstrap.py.patch

bin/buildout : bootstrap.py
	python bootstrap.py

development : bin/buildout
	bin/buildout

clean :
	rm -rf bin develop-eggs eggs parts .installed.cfg downloads bootstrap.py *.db
	find . -name "*~" -exec rm {} \;
	find . -name "DEADJOE" -exec rm {} \;
	find . -name "*.pyc" -exec rm {} \;

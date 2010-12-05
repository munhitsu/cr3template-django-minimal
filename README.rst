=======================================
cr3template-minimal-django
=======================================
Minimal template for cr3studio projects


-------------
Project start
-------------
- Download template
- edit project name in buildout.cfg
- execute make
- alter settings.py


-----------
Other steps
-----------
- configure git repository on server (fab might be of use)



-------
urls.py
-------

Minimal file::

	from django.conf.urls.defaults import patterns, include, handler500
	from django.contrib import admin
	
	admin.autodiscover()
	
	handler500 # Pyflakes
	
	urlpatterns = patterns(
	    '',
	    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
	    (r'^admin/', include(admin.site.urls)),
	    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
	)
	
	urlpatterns += patterns('',
	    (r'^', include('cms.urls')),
	)

-----------
settings.py
-----------

Minimal file::

	import os
	import socket
	
	ROOT_PATH = os.path.dirname(__file__)
	BASE_DIR = apply(os.path.join,os.path.split(ROOT_PATH)[0:-1]) #cd ..
	
	host = socket.gethostbyaddr(socket.gethostname())
	hostname = host[0].split(".")[0]
	
	HOME = os.environ['HOME']
	USER = os.environ['USER']
	
	
	INTERNAL_IPS = ('127.0.0.1',)
	DEBUG = True
	
	ADMINS = (
	    # ('Your Name', 'your_email@domain.com'),
	)
	
	MANAGERS = ADMINS
	
	HOSTCONFIG = {
	    'ichi' : {
	        'DATABASES' : {
	            'default': {
	                'ENGINE': 'django.db.backends.postgresql_psycopg2',
	                'NAME':USER,
	                'USER':USER,
	                'PASSWORD':'TBD',
	            }
	        }
	    },
	    'delta' : {
	        'DATABASES' : {
	            'default': {
	                'ENGINE': 'django.db.backends.sqlite3',
	                'NAME': 'cr3components.db'
	            }
	        }
	
	    }
	}
	
	
	
	DATABASES = HOSTCONFIG[hostname]['DATABASES']
	
	
	TIME_ZONE = 'America/Chicago'
	
	LANGUAGE_CODE = 'en-us'
	
	MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
	
	STATICFILES_ROOT = os.path.join(os.path.dirname(__file__), 'static')
	
	MEDIA_URL = '/media/'
	
	STATICFILES_URL = '/static/'
	
	ADMIN_MEDIA_PREFIX = '/admin_media/'
	
	# Don't share this with anybody.
	SECRET_KEY = '8@(!p52vohfye8l=qn@!^lybp-c#v4%i&1mo_63w+3f_!v!t*z'
	
	MIDDLEWARE_CLASSES = (
	    'django.middleware.common.CommonMiddleware',
	    'django.contrib.sessions.middleware.SessionMiddleware',
	    'django.contrib.auth.middleware.AuthenticationMiddleware',
	    'django.middleware.doc.XViewMiddleware',
	)
	
	ROOT_URLCONF = 'cr3components.urls'
	
	
	INSTALLED_APPS = (
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.admin',
	    'debug_toolbar',
	    'mptt',
	    'cr3components.cms'
	)
	
	TEMPLATE_LOADERS = (
	    'django.template.loaders.filesystem.Loader',
	    'django.template.loaders.app_directories.Loader',
	    'django.template.loaders.eggs.Loader',
	)
	
	TEMPLATE_DIRS = (
	    os.path.join(os.path.dirname(__file__), "templates"),
	)
	
	
	TEMPLATE_CONTEXT_PROCESSORS = (
	    'django.core.context_processors.debug',
	    'django.core.context_processors.i18n',
	    'django.core.context_processors.media',
	    'django.contrib.auth.context_processors.auth',
	    'django.contrib.messages.context_processors.messages',
	    'django.contrib.staticfiles.context_processors.staticfiles',
	)
	
	
	DEBUG_TOOLBAR_CONFIG = {
	    'INTERCEPT_REDIRECTS':False
	}
	
	DEBUG_TOOLBAR_PANELS = (
	    'debug_toolbar.panels.version.VersionDebugPanel',
	    'debug_toolbar.panels.timer.TimerDebugPanel',
	    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
	    'debug_toolbar.panels.headers.HeaderDebugPanel',
	    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
	    'debug_toolbar.panels.template.TemplateDebugPanel',
	    'debug_toolbar.panels.sql.SQLDebugPanel',
	    'debug_toolbar.panels.signals.SignalDebugPanel',
	    'debug_toolbar.panels.logger.LoggingPanel',
	)


----
TODO
----
make fabfile.py project independent (remote username is in there)
how to embed some settings goodies

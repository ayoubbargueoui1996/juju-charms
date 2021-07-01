#from charms.reactive import when, when_not, set_flag


#@when_not('layer-example.installed')
#def install_layer_example():
    # Do your setup here.
    #
    # If your charm has other dependencies before it can install,
    # add those as @when() clauses above., or as additional @when()
    # decorated handlers below
    #
    # See the following for information about reactive charms:
    #
    #  * https://jujucharms.com/docs/devel/developer-getting-started
    #  * https://github.com/juju-solutions/layer-basic#overview
    #
 #   set_flag('layer-example.installed')

from charms.reactive import set_flag, when, when_not
from charmhelpers.core.hookenv import application_version_set, status_set
from charmhelpers.fetch import get_upstream_version
import subprocess as sp
from charmhelpers.core.templating import render

@when_not('example.installed')
def install_example():
    set_flag('example.installed')


@when('apt.installed.hello')
def set_message_hello():
    # Set the upstream version of hello for juju status.
    application_version_set(get_upstream_version('hello'))

    # Run hello and get the message
    message = sp.check_output('hello', stderr=sp.STDOUT)

    # Set the maintenance status with a message
    status_set('maintenance', message )

    # Signal that we know the version of hello
    set_flag('hello.version.set')

@when('database.available')
def write_text_file(mysql):
    render(source='text-file.tmpl',
           target='/root/text-file.txt',
           owner='root',
           perms=0o775,
           context={
               'my_database': mysql,
           })
    status_set('active', 'Ready: File rendered.')

@when_not('database.connected')
def missing_mysql():
    status_set('blocked', 'Please add relation to MySQL')


@when('database.connected')
@when_not('database.available')
def waiting_mysql(mysql):
    status_set('waiting', 'Waiting for MySQL')

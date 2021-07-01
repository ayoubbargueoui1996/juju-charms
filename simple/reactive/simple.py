#from charms.reactive import when, when_not, set_flag


from charmhelpers.core.hookenv import ( 
     action_get, 
     action_fail, 
     action_set, 
     status_set, 
) 

from charms.reactive import ( 
     clear_flag, 
     set_flag, 
     when, 
     when_not,
) 
import charms.sshproxy

# Set the charm’s state to active so the LCM knows
# it’s ready to work.
@when('sshproxy.configured')
@when_not('simple.installed') 
def install_simple_proxy_charm():     
     set_flag('simple.installed') 
     status_set('active', 'Ready!')
# Define what to do when the `touch` primitive is invoked. 
@when('actions.touch')
def touch(): 
     err = ''
     try: 
          filename = action_get('filename') 
          cmd = ['touch {}'.format(filename)]
          result, err = charms.sshproxy._run(cmd) 
     except: 
          action_fail('command failed:' + err) 
     else: 
          action_set({'output': result})
     finally: 
          clear_flag('actions.touch')

#@when('actions.start-opensand-emulation')
#def start-opensand-emulation():
#     err = ''
#     try: 
#          port = action_get('port-opensand-cmd-server') 
#          cmd = ['telnet 127.0.0.1 {} << EOF \nstart\nsleep 5\nexit\nEOF"'.format(port)]
#          result, err = charms.sshproxy._run(cmd) 
#     except: 
#          action_fail('command failed:' + err) 
#     else: 
#          action_set({'output': result})
#     finally: 
#          clear_flag('actions.start-opensand-emulation')

#@when('actions.startOPENSANDemulation')
#def startOPENSANDemulation():



from pyad import *
from pyad.adcontainer import ADContainer
from pyad.adgroup import ADGroup
from pyad.aduser import ADUser


def addADuser():
    pyad.set_defaults(ldap_server="eden.com", username="administrator", password="Your@Password")
    ou = ADContainer.from_dn("ou=test2, dc=eden, dc=com")
    for i in range(1024):
        username = "11-22-33-44-5test."+str(i)
        aduser.ADUser.create(username, ou, password="password@123")


def addGroup():
    pyad.set_defaults(ldap_server="eden.com", username="administrator", password="Your@Password")
    ou = ADContainer.from_dn("ou=test2, dc=eden, dc=com")
    for i in range(1, 1024):
        groupname = "11-22-33-44-5testGroup" + str(i)
        ADGroup.create(groupname, ou, security_enabled=True, scope='UNIVERSAL')


def addusertogroup(user,group):
    group.add_members([user])

if __name__ == '__main__':
    addADuser()
    addGroup()
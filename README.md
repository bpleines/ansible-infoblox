dynamicInfoblox
=========

A very basic role using some of Infoblox's new integration in Core v2.5 to dynamically add a record at the next available ip

Requirements
------------

The infoblox-client installed on the targeted localhost machine. Ansible v >= 2.5 for the infoblox modules and lookup plugin

Role Variables
--------------
```
example nios_provider supplied below. This should be vaulted in vars

nios_provider:
   #Default nios_provider IP with out-of-the-box installation
   host: 192.168.1.2
   username: admin
   password: integrate
```
Dependencies
------------

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: localhost
      roles:
         - { role: dynamicInfoblox }

License
-------

BSD

Author Information
------------------

Branden Pleines

Dynamically create host records in Infoblox using Ansible!

dynamicInfoblox
=========

A basic role using some of Infoblox's new integration in Core v2.5 to dynamically add sequence of host records at the next available ip address

Requirements
------------

The infoblox-client installed on the targeted localhost machine. Ansible v >= 2.5 for the infoblox modules and lookup plugin

There is an existing dependency to manually create the reverse lookup zone- hope to resolve this soon

Role Variables
--------------
Example nios_provider supplied below. This should be vaulted for production use

```
nios_provider:
   #Out-of-the-box defaults specified here
   host: 192.168.1.2
   username: admin
   password: infoblox
```
Dependencies
------------

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: localhost
      connection: local
      roles:
         - { role: dynamicInfoblox, host_count: 10 }

This will create 10 host records at the next available IP Address

License
-------

BSD

Author Information
------------------

Branden Pleines

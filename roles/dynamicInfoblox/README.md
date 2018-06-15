Role Name
=========

A very basic role using some of infobloxes new functionality

Requirements
------------

The infoblox-client installed on the host machine. Ansible v >= 2.5 for the infoblox modules and lookup plugin

Role Variables
--------------
example nios_provider supplied below. This should be vaulted in vars

nios_provider:
  host: 192.168.0.11
  username: admin
  password: integrate

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

This is a really basic role to clone and play with as desired

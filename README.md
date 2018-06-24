Dynamically create host records in Infoblox using Ansible!

dynamicInfoblox
=========

A role using some of Infoblox's new integration in Core v2.5 to dynamically add a sequence of host records at the next available ip address. Additional functionality included to take a snapshot of the existing Gridmaster.

Requirements
------------

The infoblox-client installed on the targeted localhost machine. Ansible v >= 2.5 for the infoblox modules and lookup plugin. Wapi v2.7 required for the snapshot script.

Role Variables
--------------
Example nios_provider supplied below. This should be vaulted in /vars for production use

```
nios_provider:
   #Out-of-the-box defaults specified here
   host: 192.168.1.2
   username: admin
   password: infoblox
```
Dependencies
------------

Example Playbooks
-----------------
Role defaults can be overriden at either the playbook or role level:

```
ansible_playbook test_nios.yml -e "host_count=10"
ansible-playbook test_nios.yml -e "host_count=10 ansible_zone=redhat.com"
ansible-playbook test_nios.yml -e "host_count=10 ansible_zone=redhat.com ansible_subnet=255.255.255.0/24"
```

There is also the ability to create a snapshot of the existing configuration at any time
```
ansible_playbook test_nios.yml -e "snapshot_comment=ansible"
```

Restoring the snapshot is current a manual step but I hope to have automation here soon too.

The default invocation creates a single host in a local zone:

    - hosts: localhost
      connection: local
      roles:
         - { role: dynamicInfoblox }

Override the default host_count to create several host records at a time:

    - hosts: localhost
      connection: local
      roles:
         - { role: dynamicInfoblox, host_count: 10 }

Override the default zone:

    - hosts: localhost
      connection: local
      roles:
         - { role: dynamicInfoblox, host_count: 10, ansible_zone: redhat.com }

Override the default subnet. The default gateway_address is automated to reflect changes overriden here:

    - hosts: localhost
      connection: local
      roles:
         - { role: dynamicInfoblox, host_count: 10, ansible_zone: redhat, ansible_subnet: 255.255.255.0/24 }

License
-------

BSD

Author Information
------------------

Branden Pleines

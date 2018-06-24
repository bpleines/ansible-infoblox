Dynamically create host records in Infoblox using Ansible!

A couple roles using some of Infoblox's new integration in Core v2.5 to add a sequence of host records at the next available ip address. Additional functionality included to take a snapshot of the existing database.

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
Role defaults for dynamicInfoblox can be overriden at either the playbook or role level:

```
ansible-playbook create_dynamic_records.yml
ansible_playbook create_dynamic_records.yml -e "host_count=10"
ansible-playbook create_dynamic_records.yml -e "ansible_zone=redhat.com"
ansible-playbook ceate_dynamic_records.yml -e "ansible_subnet=10.10.10.0/24"
```

There is also the ability to create a snapshot of the existing configuration at any time
```
ansible_playbook take_snapshot.yml
```

Restoring the snapshot is current a manual step but I hope to have automation here soon too.

The default invocation creates a forward/reverse zone, subnet, and gateway address but not a record

    - hosts: localhost
      connection: local
      roles:
         - { role: dynamicInfoblox }

Specify a host_count to create several host records at a time:

    - hosts: localhost
      connection: local
      roles:
         - { role: dynamicInfoblox, host_count: 10 }

Override the default zone:

    - hosts: localhost
      connection: local
      roles:
         - { role: dynamicInfoblox, ansible_zone: redhat.com }

Override the default subnet. The default gateway_address is automated to reflect changes overriden here:

    - hosts: localhost
      connection: local
      roles:
         - { role: dynamicInfoblox, ansible_subnet: 10.10.10.0/24 }

Author Information
------------------
```
Branden Pleines
Bret Pleines
```

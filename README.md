Dynamically create host records in Infoblox using Ansible!

A collection of roles using some of Infoblox's new integration in Core v2.5 to:  1) add a sequence of host records at the next available ip address 2) start the dns service on a specified gridmaster 3) 

Requirements
------------

The infoblox-client installed on the targeted localhost machine. Ansible Core >= v2.5 for the infoblox modules and lookup plugin. Wapi v2.7 required for the snapshot script.

Role Variables
--------------
Example nios_provider supplied below. This should be vaulted in /group_vars/all for production use

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
ansible-playbook create_dynamic_records.yml -e "host_count=10"
ansible-playbook create_dynamic_records.yml -e "ansible_zone=redhat.com"
ansible-playbook create_dynamic_records.yml -e "ansible_subnet=10.10.10.0/24"
```

An additional playbook is included to start the dns service on the gridmaster
```
ansible-playbook start_dns_service.yml -e 'gridmaster_fqdn=192.168.1.2'
```

There is also the ability to create a snapshot of the database at any time
```
ansible-playbook take_snapshot.yml
```

Restoring the snapshot is current a manual step but I hope to have automation here soon too.

A final playbook requires a second configured Infoblox instance. It provisions the second instance as a gridmaster candidate. It requires 4 variables to be defined: 1) master_candidate_name, 2) master_candidate_address, 3) master_candidate_gateway, 4) master_candidate_subnet_mask
```
ansible-playbook provision_gridmaster_candidate.yml -e 'master_candidate_name=gmc.ansible.local master_candidate_address=192.168.2.2, master_candidate_gateway=192.168.2.254, master_candidate_subnet_mask=255.255.255.0'
```

The default invocation creates a forward/reverse zone, subnet, and gateway address but not any records

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

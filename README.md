Dynamically create host records in Infoblox using Ansible!

A collection of roles featuring some of Infoblox's new integration in Core v2.5 to: 
1. Add a sequence of host records at the next available ip address 
2. Update a service
3. Take a configuration snapshot
4. Provision a gridmaster member

Requirements
------------

The infoblox-client installed on the targeted localhost machine. Ansible Core >= v2.5 for the infoblox modules and lookup plugin. Wapi v2.7 required for the snapshot script.

Role Variables
--------------
Example nios_provider supplied below. This should be vaulted in /group_vars/localhost/main.yml for production use

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

An additional playbook is included to publish updates to gridmember services:
```
ansible-playbook update_service.yml -e 'gridmember_fqdn=192.168.1.2 state=started'
ansible-playbook update_service.yml -e 'gridmember_fqdn=192.168.1.2 state=restarted service_option=ALL'
ansible-playbook update_service.yml -e 'gridmember_fqdn=192.168.1.2 state=restarted service_option=DHCP'
ansible-playbook update_service.yml -e 'gridmember_fqdn=192.168.1.2 state=restarted service_option=DNS'
```

There is also the ability to create a snapshot of the gridmaster configuration at any time:
```
ansible-playbook take_snapshot.yml
```

Note: Restoring the snapshot is currently a manual step but I hope to have automation here soon too.

A final playbook requires a second configured Infoblox instance. It provisions the second instance as a gridmaster candidate assuming nios_provider as the gridmaster. It requires 4 variables to be defined: 
1. master_candidate_name
2. master_candidate_address
3. master_candidate_gateway
4. master_candidate_subnet_mask
```
ansible-playbook provision_gridmaster_candidate.yml -e 'master_candidate_name=gmc.ansible.local master_candidate_address=192.168.2.2 master_candidate_gateway=192.168.2.254 master_candidate_subnet_mask=255.255.255.0'
```

Role Calls
-----------------
Overrides at the role level allow single playbooks to call the same roles in succession with new network information.

The default invocation creates a forward/reverse zone, subnet, and gateway address using out-of-the-box configurations, but does not generate additional hosts:

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

Start the dns service on a specified gridmember:

    - hosts: localhost
      connection: local
      roles:
         - { role: updateService, gridmember_fqdn: 192.168.1.2, state: started }

Restart only the dhcp service on a specified gridmember:

    - hosts: localhost
      connection: local
      roles:
         - { role: uppdateService, gridmember_fqdn: 192.168.1.2, state: restarted, service_option: DHCP }

Restart only the dns service on a specified gridmember:

    - hosts: localhost
      connection: local
      roles:
         - { role: updateService, gridmember_fqdn: 192.168.1.2, state: restarted, service_option: DNS }

Restart dhcp and dns service on a specified gridmember:

    - hosts: localhost
      connection: local
      roles:
         - { role: updateService, gridmember_fqdn: 192.168.1.2, state: restarted, service_option: ALL }

Take a snapshot of Infoblox configuration:

    - hosts: localhost
      connection: local
      roles:
         - { role: snapshotConfiguration }

Provision a new gridmaster candidate:

    - hosts: localhost
      connection: local
      roles:
         - { role: provisionGridmasterCandidate, master_candidate_name:gmc.ansible.local, master_candidate_address: 192.168.2.2, master_candidate_gateway: 192.168.2.254, master_candidate_subnet_mask:255.255.255.0 }


Author Information
------------------
```
Branden Pleines
Bret Pleines
```

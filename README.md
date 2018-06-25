Dynamically create host records in Infoblox using Ansible!

A collection of roles featuring some of Infoblox's new integration in Core v2.5 to: 
1. Add a sequence of host records at the next available ip address 
2. Restart the DNS service on the gridmaster
3. Take a configuration snapshot
4. Provision a gridmaster candidate
5. Provision a gridmember

Requirements
------------

The infoblox-client installed on the targeted localhost machine. Ansible Core >= v2.5 for the infoblox modules and lookup plugin. Content tested using *WAPI v2.7*.

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

Example Playbooks
-----------------
Role defaults for dynamicInfoblox can be overriden at either the playbook or role level:

```
ansible-playbook create_dynamic_records.yml
ansible-playbook create_dynamic_records.yml -e "host_count=10"
ansible-playbook create_dynamic_records.yml -e "ansible_zone=redhat.com"
ansible-playbook create_dynamic_records.yml -e "ansible_subnet=10.10.10.0/24"
```

The following playbook invocation starts the DNS service on the gridmaster:
```
ansible-playbook update_service.yml -e 'gridmaster_fqdn=gm.ansible.local state=started'
```

***Work in Progress***A slightly different invocation of this same playbook will restart the gridmaster service specified
```
ansible-playbook update_service.yml -e 'state=restarted service_option=ALL'
ansible-playbook update_service.yml -e 'state=restarted service_option=DHCP'
ansible-playbook update_service.yml -e 'state=restarted service_option=DNS'
```

There is also the ability to create a snapshot of the gridmaster configuration at any time:
```
ansible-playbook take_snapshot.yml
```

Note: Restoring the snapshot is currently a manual step but I hope to have automation here soon too.

These final playbooks require a second configured Infoblox instance. 

This first playbook provisions the second instance as a gridmaster candidate assuming nios_provider as the gridmaster. It requires 4 variables to be defined: 
1. master_candidate_name
2. master_candidate_address
3. master_candidate_gateway
4. master_candidate_subnet_mask
```
ansible-playbook provision_gridmaster_candidate.yml -e 'master_candidate_name=gmc.ansible.local master_candidate_address=192.168.2.2 master_candidate_gateway=192.168.2.254 master_candidate_subnet_mask=255.255.255.0'
```

This one provisions a grid member. It requires 4 variables to be defined:
1. member_name
2. member_address
3. member_gateway
4. member_subnet_mask
```
ansible-playbook provision_gridmember.yml -e 'member_name=m3.ansible.local member_address=192.168.2.3 member_gateway=192.168.2.254 member_subnet_mask=255.255.255.0'
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
         - { role: updateService, gridmaster_fqdn=gm.ansible.local, state: started }

Force Restart - only the dhcp service on a specified gridmember:

    - hosts: localhost
      connection: local
      roles:
         - { role: uppdateService, state: restarted, service_option: DHCP }

Force restart - only the dns service on a specified gridmember:

    - hosts: localhost
      connection: local
      roles:
         - { role: updateService, state: restarted, service_option: DNS }

Force restart - dhcp and dns service on a specified gridmember:

    - hosts: localhost
      connection: local
      roles:
         - { role: updateService, state: restarted, service_option: ALL }

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


Provision a new gridmember:

    - hosts: localhost
      connection: local
      roles:
         - { role: provisionGridmember, member_name:gmc.ansible.local, member_address: 192.168.2.2, member_gateway: 192.168.2.254, member_subnet_mask:255.255.255.0 }

Author Information
------------------
```
Branden Pleines
Bret Pleines
```

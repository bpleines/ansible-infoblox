Dynamically create host records in Infoblox using Ansible!

A collection of roles featuring some of Infoblox's new integration in Core v2.5 to: 
1. Create zones and add host records at the next available ip addresses using a Name Server Group
2. Start the DNS service on the Grid Master
3. Predefine a Grid Master Candidate
4. Predefine a Grid Member
5. Join a Grid Master Candidate or Grid Member to a Grid
6. Update a Name Server Group to account for new Infoblox Grid appliances
7. Take a configuration snapshot

Requirements
------------

The infoblox-client installed on the targeted localhost machine. Ansible Core >= v2.5 for the Infoblox modules and lookup plugin.

Role Variables
--------------
Example *nios_provider* supplied below. *nios_provider* can be vaulted in group_vars/all/vault.yml for production use.

```
nios_provider:
   #Out-of-the-box defaults specified here
   host: 192.168.1.2
   username: admin
   password: infoblox

wapi_version: 'v2.6'
```

Example Playbooks
-----------------
Most automation functionality in this repository is better demonstrated by calling of roles (see below), but each role has a corresponding playbook that can be called for the same effect.

Here are some of the common overrides at the playbook level of this repository's core role, dynamicInfoblox:

```
ansible-playbook create_dynamic_records.yml
ansible-playbook create_dynamic_records.yml -e "host_count=10"
ansible-playbook create_dynamic_records.yml -e "ansible_zone=redhat.com"
ansible-playbook create_dynamic_records.yml -e "ansible_subnet=10.10.10.0/24"
```

Another example playbook creates a snapshot of the Grid Master configuration at any time:
```
ansible-playbook take_snapshot.yml
```
_Note: Restoring the snapshot is currently a manual step but I hope to have automation here soon too._

This calls a master playbook to demo the invocation of several roles in succession:
```
ansible-playbook master-demo-playbook.yml
```

Role Calls
-----------------
Overrides at the role level allow single playbooks to call the same roles in succession with new network information.

The default invocation creates a forward/reverse zone, subnet, and gateway address using out-of-the-box configurations, but does not generate additional hosts:
```yaml
    - hosts: localhost
      connection: local
      roles:
         - { role: dynamicInfoblox }
```
Specify a *host_count* to create (several) new host records at a time:
```yaml
         - { role: dynamicInfoblox, host_count: 10 }
```
Override the default zone:
```yaml
         - { role: dynamicInfoblox, ansible_zone: redhat.com }
```
Override the default subnet. The default *gateway_address* is automated to reflect changes overriden here:
```yaml
         - { role: dynamicInfoblox, ansible_subnet: 10.10.10.0/24 }
```
Start the dns service on an Infoblox appliance:
```yaml
         - { role: updateService, grid_fqdn: gm.ansible.local, state: started }
```
Predefine a new Grid Master Candidate:
```yaml
         - { role: predefineGridmasterCandidate, master_candidate_name: gmc.ansible.local, master_candidate_address: 192.168.2.2, master_candidate_gateway: 192.168.2.254, master_candidate_subnet_mask: 255.255.255.0 }
```
Predefine a new Grid Member:
```yaml
         - { role: predefineGridmember, member_name: m3.redhat.com, member_address: 192.168.2.3, member_gateway: 192.168.2.254, member_subnet_mask: 255.255.255.0 }
```
Join a Grid Master Candidate or Grid Member to the Grid:
```yaml         
         - { role: joinGrid, join_grid_host: 192.168.2.3 }
```         
Take a snapshot of Infoblox configuration:
```yaml
         - { role: snapshotConfiguration }
```

Author Information
------------------
```
Branden Pleines
Bret Pleines
```

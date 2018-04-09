The following content is an ongoing effort to test the new integration between Infoblox and Ansible Core v2.5

The nios_provider variable used in the tasks is intentionally encrypted to reflect a proper project setup. The cotents in that encrypted file look like the following:

---vars/main.yml---
---
nios_provider:<br>
(indent)host: 192.168.0.11<br>
(indent)username: admin<br>
(indent)password: integrate<br>

<i>More content to follow</i>

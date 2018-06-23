def subnet_to_gateway(ipAddress):
    ip_components = ipAddress.split('.')
    return ip_components[0] + '.' +  ip_components[1] + '.' + ip_components[2]

def strip_cidr(subnet):
    ip_components = subnet.split('.')
    final, cidr = ip_components[3].split('\\')
    return ip_components[0] + '.' +  ip_components[1] + '.' + ip_components[2] + '.' + final

class FilterModule(object):
    def filters(self):
        return {
            'subnet_to_gateway': subnet_to_gateway,
            'strip_cidr': strip_cidr
            }

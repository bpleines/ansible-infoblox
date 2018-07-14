def subnet_to_gateway(ipAddress):
    ip_components = ipAddress.split('.')
    return ip_components[0] + '.' +  ip_components[1] + '.' + ip_components[2]

class FilterModule(object):
    def filters(self):
        return {
            'subnet_to_gateway': subnet_to_gateway
            }

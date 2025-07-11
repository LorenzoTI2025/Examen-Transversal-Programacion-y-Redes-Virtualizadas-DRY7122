from ncclient import manager
import xml.dom.minidom

# Conexión al router CSR1000v vía NETCONF
m = manager.connect(
    host="192.168.56.119",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)

# Configuración para cambiar el hostname
netconf_hostname = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>LOPEZx2-GOMEZ-FUENTES</hostname>
  </native>
</config>
"""

# Aplicar configuración
netconf_reply = m.edit_config(target="running", config=netconf_hostname)

# Mostrar respuesta
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

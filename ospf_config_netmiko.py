from netmiko import ConnectHandler

# Datos de conexión al CSR1000v
csr1000v = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.101',     #
    'username': 'cisco',
    'password': 'cisco123!',
    #'secret': 'cisco'             
}

# Conexión
net_connect = ConnectHandler(**csr1000v)
net_connect.enable()

# --- CONFIGURACIÓN OSPF IPv4 ---
config_ipv4 = [
    'router ospf 1',
    'router-id 1.1.1.1',
    'network 192.168.56.0 0.0.0.255 area 0',
    'passive-interface default',
    'no passive-interface GigabitEthernet1',
]

# --- CONFIGURACIÓN OSPF IPv6 ---
config_ipv6 = [
    'interface GigabitEthernet1',
    'ipv6 enable',
    'ipv6 ospf 1 area 0',
    'exit',
    'ipv6 router ospf 1',
    'router-id 2.2.2.2',
    'passive-interface default',
    'no passive-interface GigabitEthernet1',
]

# Enviar configuración
print("\n🔧 Configurando OSPF IPv4...")
net_connect.send_config_set(config_ipv4)

print("🔧 Configurando OSPF IPv6...")
net_connect.send_config_set(config_ipv6)

# --- Obtener y guardar resultados ---
outputs = {
    "ospf_config.txt": net_connect.send_command("show running-config | section ospf"),
    "ip_interface_brief.txt": net_connect.send_command("show ip interface brief"),
    "ipv6_interface_brief.txt": net_connect.send_command("show ipv6 interface brief"),
    "ip_interface.txt": net_connect.send_command("show ip interface"),
    "ipv6_interface.txt": net_connect.send_command("show ipv6 interface"),
    "running_config.txt": net_connect.send_command("show running-config"),
    "version_info.txt": net_connect.send_command("show version"),
}

# Mostrar y guardar cada salida
for filename, output in outputs.items():
    print(f"\n📄 {filename}\n")
    print(output)
    with open(filename, "w") as f:
        f.write(output)

# Cerrar conexión
net_connect.disconnect()

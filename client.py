import socket
import ssl

# Configuration du client
server_address = ('192.168.170.124', 8888)

# Créer un socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wrap the socket in SSL
ssl_socket = ssl.wrap_socket(client_socket, cert_reqs=ssl.CERT_REQUIRED, ca_certs="chemin/vers/votre_certificat.crt",
                             ssl_version=ssl.PROTOCOL_TLSv1_2)

try:
    # Connecter le client au serveur
    ssl_socket.connect(server_address)

    # Envoyer des données au serveur
    message = 'Bonjour, serveur!'
    ssl_socket.sendall(message.encode('utf-8'))
    print('Données envoyées:', message)

    # Recevoir la réponse du serveur
    data = ssl_socket.recv(1024)
    print('Réponse du serveur:', data.decode('utf-8'))

finally:
    # Fermer la connexion
    ssl_socket.close()

import socket
import ssl

# Charger le certificat du serveur
server_cert = "serveur_http.cert.pem"
server_key = "serveur_http.pem"

# Configuration du serveur
server_address = ('127.0.0.1', 8888)

# Créer un socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(1)

print('Le serveur écoute sur {}:{}'.format(*server_address))

while True:
    print('En attente de la connexion...')
    client_socket, client_address = server_socket.accept()

    # Wrap the socket in SSL
    ssl_socket = ssl.wrap_socket(client_socket, keyfile=server_key, certfile=server_cert, server_side=True,
                                 cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLSv1_2)

    print('Connexion depuis', client_address)

    try:
        # Lire les données du client
        data = ssl_socket.recv(1024)
        print('Données reçues:', data.decode('utf-8'))

        # Envoyer une réponse
        ssl_socket.sendall('Message reçu par le serveur'.encode('utf-8'))

    finally:
        # Fermer la connexion
        ssl_socket.close()

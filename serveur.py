import socket
import ssl

# Paramètres du serveur
HOST = '127.0.0.1'  # Adresse IP du serveur
PORT = 12345         # Port d'écoute du serveur
CERTFILE = 'serveur_http.cert.pem'  # Chemin vers le certificat du serveur
KEYFILE = 'serveur_http.pem'   # Chemin vers la clé privée du serveur

# Création du socket serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Le serveur écoute sur {HOST}:{PORT}")

# Initialisation de secure_client_socket en dehors du bloc try
secure_client_socket = None

try:
    # Attente de la connexion d'un client
    client_socket, client_address = server_socket.accept()
    print(f"Connexion établie avec {client_address}")

    # Wrapping du socket dans SSL
    secure_client_socket = ssl.wrap_socket(
        client_socket, keyfile=KEYFILE, certfile=CERTFILE, server_side=True)

    # Envoi du certificat au client
    with open(CERTFILE, 'rb') as cert_file:
        server_cert_bytes = cert_file.read()

    secure_client_socket.send(server_cert_bytes)

    while True:
        # Attente de données depuis le client
        data = secure_client_socket.recv(1024).decode('utf-8')

        if not data:
            break

        print(f"Client: {data}")

        # Réponse au client
        message = input("Serveur: ")
        secure_client_socket.send(message.encode('utf-8'))

except ssl.SSLError as e:
    print(f"Une erreur SSL s'est produite : {e}")

except Exception as e:
    print(f"Une erreur inattendue s'est produite : {e}")

finally:
    # Fermeture des connexions
    if secure_client_socket:
        secure_client_socket.close()

    server_socket.close()
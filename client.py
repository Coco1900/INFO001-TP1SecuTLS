import socket
import ssl
import sys
from cryptography import x509
from cryptography.hazmat.backends import default_backend

# Paramètres du client
HOST = 'www.pagin.fr'  # Adresse IP du serveur
PORT = 12345         # Port d'écoute du serveur

# Création du socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Création du contexte SSL
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

# Ajout de la vérification du certificat en spécifiant le fichier de certificat de l'émetteur (Root CA)
context.load_verify_locations(cafile='root-ca-lorne.pem')

# Wrapping du socket dans SSL en utilisant le contexte SSL
secure_client_socket = context.wrap_socket(client_socket, server_hostname=HOST)

# Réception du certificat du serveur
server_cert_bytes = secure_client_socket.recv(4096)
server_cert = x509.load_pem_x509_certificate(
    server_cert_bytes, default_backend())

# Vérification du certificat

# Ajoutez ici votre logique de vérification du certificat (nom de domaine, date, CA, etc.)
print(f"Certificat du serveur décodé:\n{server_cert}")

# Extraction du Common Name (CN) du certificat
common_name = server_cert.subject.get_attributes_for_oid(
    x509.NameOID.COMMON_NAME)[0].value

# Comparaison avec la variable HOST
if common_name == HOST:
    print(f"Le Common Name (CN) du certificat correspond à {HOST}")
else:
    print(f"Le Common Name (CN) du certificat ne correspond pas à {HOST}")
    # Annulation de la connexion
    secure_client_socket.close()
    sys.exit("La connexion est annulée en raison d'une non-correspondance du Common Name (CN).")


while True:
    # Envoi de données au serveur
    message = input("Client: ")
    secure_client_socket.send(message.encode('utf-8'))

    # Attente de la réponse du serveur
    data = secure_client_socket.recv(1024).decode('utf-8')
    print(f"Serveur: {data}")

# Fermeture de la connexion
secure_client_socket.close()
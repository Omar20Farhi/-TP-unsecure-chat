## ANSWERS.md - TP Unsecure Chat

### 1. Que pensez-vous de la confidentialité des données vis à vis du serveur ?
Les données ne sont pas chiffrées. Le serveur peut lire tous les messages.

### 2. Pouvez-vous expliquer en quoi la sérialisation pickle est certainement le plus mauvais choix ?
Pickle permet l’exécution de code à la désérialisation via `__reduce__`, ce qui est dangereux.

### 3. Quels types de sérialisation pourrait-on utiliser pour éviter cela ? (hors CVE)
Utiliser `json` ou `msgpack`, qui ne permettent pas l’exécution de code.

### 4. Pourquoi le chiffrement seul est-il insuffisant ?
Le chiffrement ne garantit pas l’intégrité ni l’authenticité du message.

### 5. Quelle fonction(s?) en python permet de générer un salt avec une qualité cryptographique ?
`secrets.token_bytes()` ou `os.urandom()`

### 6. Faudra-t-il transmettre le salt comme champ en clair supplémentaire du paquet message ?
Oui.

### 7. Quelles variables faut-il amender dans le constructeur pour utiliser `msgpack` au lieu de `pickle` dans AEServer ?
`self._serial_function = msgpack.packb` et `self._deserial_function = msgpack.unpackb`

### 8. Que faudrait-il faire en théorie pour éviter l’action du rogue server ?
Utiliser un chiffrage avec AEAD pour authentifier le message et son contexte (comme le `nick`).

### 9. Pourquoi Fernet n’est pas adapté dans ce cadre ?
Fernet ne supporte pas AEAD. Il ne chiffre que les données, sans associer d’autres données à vérifier.



# AutoOSINT

## Mettre en place l'application

### Pour que l'installeur marche, il est nécessaire d'utiliser Python 3 et aptitude pour les paquets.

### Il faut dans un premier temps installer les dépendances requises.
```
./install.sh
```

## Faire marcher Shodan

### Pour que Shodan puisse marcher dans l'application, il vous faut une clé d'API. Une fois que vous l'avez récupérer, tapez : 
```
echo -n <api_key> | tee shodan_api.key
```

### Il faut également indiquer à theHarvester votre clé d'API. 
```
nano /etc/theHarvester/api_keys.yaml

```
### Et insérer la clé dans
```
shodan:
    key: <api_key>
```
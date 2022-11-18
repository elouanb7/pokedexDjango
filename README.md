# pokedexDjango

### Utilisateur admin

username : chen  
email : professeurchen@elouanb7.com  
password : profchen  

### Récuperer le projet

Allez sur ce lien : https://github.com/elouanb7/pokedexDjango.git  
et cloner le projet dans vos dossier

### IDE

Ouvrez le projet dans votre IDE de votre choix

### Environnement Virtuel

Si votre IDE ne met pas en place un environnement virtuel,  
vous devez en mettre un. Pour ce faire, ouvrez un terminal a la racine de votre projet  
et tapez les commandes suivantes :  

- Si vous avez besoin d'installer un environnement virtuel :
````shell
$ pip install virtualenv
````

- Pour créer un venv :
`````shell
$ py -m venv [NomduVenv]
`````

- Pour activer le venv, aller dans le dossier script dans le venv et faites la commande suivante:
````shell
$ ./activate
````

- Pour désactiver le venv :
````shell
$ ./deactivate
````

### Lancer le projet

- Pour lancer le projet, aller a la racine du projet et tapez la commande suivante :
````shell
py ./manage.py runserver
````

La commande devrait vous retourner des informations et notamment une url.  
Vous devrez avoir une url qui ressemble à "http://127.0.0.1:8000/"

A la suite, rajouter "pokedex/1" afin de voir le premier pokemon
# Jus de Pomme
Une application Web pour gérer l'événement "Jus de Pomme" sans trop se casser la tête !

## Présentation

### Organisation
Le projet est divisé en deux parties :
- L'API, qui contient toutes les données et les distribue
- L'application Web, qui est l'interface à laquelle les utilisateurs peuvent accéder

Les principaux outils utilisés sont :
- Python, nécessaire au fonctionnement des deux parties
- FastAPI, utilisé pour la création de l'API
- Flask, utilisé pour la création de l'application Web

Le projet a été créé, imaginé et développé par Bidulman dans le cadre de l'événement "Jus de Pomme", où des personnes amènent des pommes (comptées en Kg), les pressent et doivent repartir avec une dose de jus de pomme (comptée en L) proportionnelle à la quantité de pommes amenée, ainsi que la rentabilité des pommes (comptée en L/Kg).


### But du projet
- "Page d'Accueil" qui permet à tout le monde de visualiser les pressées
- "Connexion" qui donne accès à un système d'authentification pour se connecter en tant qu'admin, manager ou investor
- "Panel Admin" pour les admin, où nous pouvons créer et supprimer des utilisateurs
- "Panel Manager" pour les managers, où nous pouvons gérer les pressées (pommes utilisées, jus produit)
- "Panel Investor"
  - pour les investors, qui peuvent depuis ici visualiser combien ils peuvent emporter de jus à la fin des pressages
  - pour les managers, qui peuvent voir combien de jus de pomme doit être redistribué

### Utilisation
Bien que le projet soit ouvert à tous, il n'a été développé que pour son propriétaire. Le projet ne sera donc pas documenté sur la partie "déploiement".


## Conclusion

Le projet a donc été développé dans le but de décharger les reponsabilités de "l'agent comptable" de l'événement "Jus de Pomme", qui n'a maintenant plus qu'à entrer des nombres sur son téléphone portable, sans besoin de calculer. On appelle aussi ça "la flemme", mais ça ne faisait pas très beau dans une présentation de projet sérieux.
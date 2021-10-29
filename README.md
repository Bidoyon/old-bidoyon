# Jus de Pomme
Une application Web pour gérer l'événement "Jus de Pomme" sans trop se casser la tête !

## Présentation

### L'événement
Le projet a été créé pour faciliter la gestion de l'événement "Jus de Pomme". Lors de cet événement dans le village, un grand pressoir est installé. Chacun participe à l'achat d'une certaine partie des pommes, ces participants sont appelés les **investisseurs**, simplement car ils placent des pommes pour recevoir plus tard une dose de jus de pomme proportionnelle à ce qu'ils ont apporté comme pommes. L'événement est découpé en plusieurs **pressées** : on remplit le pressoir d'une certaine dose de pommes, on presse, et on récupère le jus produit. Chaque pressée peut donc avoir une **quantité différente de pommes** (comptée en Kg), et donc une **quantité différente de jus** produit (comptée en L). On compte ensuite le nombre de **jus contenu dans les pommes** (compté en L/Kg). En moyenne, les pommes utilisées produisent environ 0.6 L/Kg. Ces valeurs sont évidemment approximatives !

### Le but du projet
Cet événement implique donc plusieurs calculs. Les investisseurs doivent recevoir une part de jus de pomme proportionnelle à la quantité de pommes qu'ils ont apporté. Pour obtenir le nombre de jus qu'ils récupèreront, on effectue le calcul **I÷T×P**, où I est le nombre de pommes amené par l'investisseur (Kg), T est le nombre total de pommes apporté par les investisseurs (Kg), et P est la quantité de jus produite sur tout l'événement (L). On obtient alors la quantité de jus de pomme que doit recevoir l'investisseur (L). De plus, nous devons garder un œil sur la quantité de jus produite, les pommes utilisées, les pommes restantes ainsi que la quantité de jus dans les pommes, **dans chaque pressée et au total** !

Le projet est donc là pour faciliter la gestion de l'événement. Il doit être capable de fournir une interface utilisateur (sous forme de site Web) facile d'accès, avec un système de comptes et d'authentification, de plusieurs rôles (ils seront détaillés plus bas) et donc de permissions. Il doit effectuer les calculs automatiquement à partir des valeurs qu'on y rentre, et les afficher de différentes façons en fonction du rôle de l'utilisateur.

## Le projet

### Organisation
Pour assurer un développement simple et fiable, le projet est divisé en deux parties ayant des difficultés bien distinctes :
- L'application Web, accessible par n'importe qui, affiche les données et fait l'intermédiaire entre l'API.
- L'API, aussi appelée le "Service de Données" est chargée de stocker la base de données et de permettre un accès aux informations à travers des requêtes HTTP.

### Outils utilisés
Pour fonctionner, le projet se base sur un langage et des libraires.
- Python est le langage utilisé pour les deux services (Web et API)
- HTML est utilisé pour la structuration des pages (accompagné de CSS)
- Flask est la librairie utilisée pour l'application Web
- FastAPI est la librairie utilisée pour l'API
- Sqlite3 s'occupe de stocker les données de l'API
- Requests permet aux deux services de communiquer entre eux
- Waitress et Uvicorn sont utilisées pour exécuter les deux services

D'autres librairies préinstallées dans l'installation basique de Python sont utilisées certaines fois, mais je juge inutile d'en parler ici, puisqu'elles sont utilisées dans pratiquement tous les projets.

### Création
Le projet a été créé, imaginé et développé par Bidulman seul, même si je serais plutôt tenté de dire que Google a grandement participé au projet, puisqu'il a subi plus d'une centaine de recherches durant tout le développement du projet.

### Utilisation
Le projet étant publié sur GitHub, libre à vous de l'utiliser si vous veniez à produire du jus de pomme dans la cour de votre maison. Mais le projet a été créé seulement pour un événement en particulier. Il se peut qu'il ne soit donc pas adapté à votre propre événement. Une documentation et une présentation d'utilisation n'est donc pas prévue pour ce projet. Débrouillez-vous ! Aussi, certains fichiers ont été ajoutés au dépôt de code puisqu'ils sont nécessaires au déploiement de l'application, mais sont inutiles si vous ne déployez pas le projet.

### Structure
Cette partie permet d'expliquer rapidement comment est structuré le projet, ce n'est pas une documentation à proprement parler.

#### Utilisateurs
Les utilisateurs sont divisés en trois parties : les admins, les managers et les investors (en Français : les administrateurs, les responsables et les investisseurs). Chaque rôle peut accéder à ses avantages, ainsi qu'aux avantages des rôles en dessous de lui.
- L'administrateur peut créer et supprimer des utilisateurs avec n'importe laquelle des permissions citées ci-dessus.
- Le responsable peut gérer les pressées : il peut en ajouter, les modifier (changer le nombre de pommes utilisées à l'intérieur et la quantité de jus produit). Il accède aussi aux investissements des investisseurs (il peut les consulter et les modifier). Attention : il ne peut consulter et modifier les investissements des utilisateurs que des utilisateurs existants ! Seul l'administrateur peut ajouter un utilisateur.
- L'investisseur peut consulter son investissement. Il peut voir combien de pommes il a investi (il ne peut pas le modifier), et combien son investissement lui rapporte jusqu'ici.

Un visiteur du site qui n'est pas connecté ou même inscrit n'est pas compté comme un utilisateur. Même s'il possède des permissions : il peut accéder à la page d'accueil et peut donc visualiser l'état des pressées.

#### Différentes pages
- La page d'accueil qui permet à tout le monde de visualiser les pressées
- La page de connexion qui permet aux utilisateurs de se connecter
- Le panel admin, qui permet aux administrateurs de créer ou de supprimer des utilisateurs
- Le panel manager, qui permet aux responsables de gérer les pressées
- Le panel investor qui permet
  - aux investisseurs de visualiser leurs investissements et ce que ça leur rapporte
  - aux responsables de voir combien de pommes ont été investies, le jus à redistribuer...

## Comment ça marche ?
Si je venais à devoir faire un système similaire par la suite, cette partie me servirait. Elle expliquera différentes façons de procéder que j'utilise dans l'application. Ces façons de procéder sont très loin d'être les meilleures, mais elles ont l'avantage d'être simples et rapide à utiliser : pour un projet qui doit être imaginé, développé et déployé en peu de jours, c'est plutôt pratique.

Cette partie sera essentiellement rédigée à la première personne, car il s'agit de mon ressenti. Votre avis peut totalement différer du mien, il existe bien plus d'une façon de faire en code.

Dans les textes qui vont suivre, j'utiliserai plutôt "application" pour parler de l'application web, et "API" pour parler... de l'API !

### L'authentification
S'il y a bien une chose que j'ai pensé lorsque j'ai décidé de créer cette application, c'est bien sûr l'authentification.

Tout d'abord, ce qu'il faut savoir, c'est que l'événement "Jus de Pomme" se limite à une vingtaine de personnes, dont beaucoup de couples et d'enfants. Pour moi, pas besoin d'inscription : je peux très bien m'occuper de créer des comptes aux personnes qui en ont besoin ! Mais qui dit "compte" dit "connexion". Alors même s'il n'y a pas besoin d'une page d'inscription, il y a bien besoin d'une page de connexion !

Pour se connecter, on remplit un formulaire avec son nom d'utilisateur et son mot de passe. Quand on clique sur le bouton, les données ne vont pas directement à l'API. La requête POST générée par le formulaire est d'abord traitée par l'application qui récupère les données du formulaire et les ordonne dans un format JSON. (Voir partie "Les formulaires" pour plus d'informations)

Elle envoie ensuite les données qu'elle a mises en forme sous la forme d'une requête GET à l'API. Cette requête contient donc par exemple les données {"username": "Bidulman", "password": "ILoveCoding"}. En réponse à cette requête, l'API renvoie des informations sur l'utilisateur : son **nom d'utilisateur** (qu'on soit sûrs que c'est bien lui, on ne sait jamais !), **son rôle** (ou sa permission, si vous préférez) ainsi que **son token**.

Si l'authentification est réussie, alors l'application va rediriger l'utilisateur sur son panel de base (s'il est responsable, il sera redirigé sur le panel manager).

Ce qui nous intéresse pour l'instant, c'est ce fameux token, le "jeton d'authentification". Ce jeton est un token hexadécimal en 16 bits du module **secrets**, c'est-à-dire une suite de 32 caractères compris entre **a et b** ou **0 et 9**.

Au lieu d'envoyer le nom d'utilisateur et le mot de passe à l'API à chaque fois que l'utilisateur change de page, je préfère envoyer un token. C'est bien plus pratique d'envoyer une seule valeur à l'API. En plus, c'est très simple de passer un petit token de page en page : il suffit de l'ajouter en argument à l'URL que l'utilisateur demande.

Ce token est **indispensable** pour une bonne navigation sur l'application, car la plupart des pages ont besoin que l'utilisateur soit authentifié.

Mais finalement, comment ça marche dans le code ? Tout simplement, l'application envoie le token à l'API. L'API va chercher l'utilisateur qui possède ce token dans sa base de données et va retourner son nom et sa permission.

À partir de ces précieuses informations, l'application va comparer la permission requise par la page avec la permission que possède l'utilisateur. Si l'utilisateur a la bonne permission, l'application lui charge la page. Sinon, elle lui envoie une erreur.

### Les formulaires
Toute donnée à rentrer, toute action que l'utilisateur exécute est remplie sous forme de formulaire. Authentification, ajout ou suppression d'utilisateur, ajout ou édition de pressée : tout passe par un formulaire.

Ce formulaire n'est pas traité par l'API. Du moins, pas directement. Une fois le formulaire rempli et envoyé, une requête POST contenant toutes les informations du formulaire est envoyée à une autre route de l'application Web, invisible du point de vue du visiteur. L'application récupère les données et les réorganise pour envoyer une requête à l'API, qui lui répond.

L'application peut alors renvoyer l'utilisateur sur une autre page, souvent un message de confirmation.

### L'avancement
Cette partie n'a pas vraiment de rapport avec comment marche l'application, mais plutôt comment je fonctionne.

Malgré le fait que ce projet m'ait motivé, je devais le terminer en seulement quelques jours. Comme à mon habitude, j'ai rencontré énormément de problèmes, des erreurs, même des fois un "s" manquant dans une base de données et tout plante.

Et contrairement à ce qu'on pourrait croire, ma "flemme de corriger ça maintenant" n'a pas été un frein. Au lieu de batailler inutilement sur un problème, j'ai pu continuer d'autres branches de l'application qui ne dépendaient pas de la partie défaillante.

L'important quand on a la flemme, c'est simplement de noter ce qu'on a à faire sur une feuille de papier. Effectivement, malgré mes deux To Do List bien remplies, j'ai trouvé la motivation pour tout corriger le lendemain.

Le secret, c'est de savoir faire autre chose sans perdre de vue son objectif.

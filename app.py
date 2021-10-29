from flask import Flask, render_template, request, redirect

import requests
import json

app = Flask(__name__)

# Address of this webapp (WITHOUT THE END SLASH)
address = "https://juspomme.herokuapp.com"
# Address of the API (WITHOUT THE END SLASH TOO)
api_address = "http://40.118.48.81:8000"


def message(text, panel, token):
    """
    Returns a message template
    """
    # Render the template en return it
    return render_template('message.html', text=text, address=address, panel=panel, token=token)


def requires_api(f):
    """
    Decorator which tries to request the API to check if API is alive
    """

    # Define the wrapper
    def wrapper():
        # Try to request the API
        try: requests.get(api_address)
        # If API doesn't respond
        except requests.exceptions.ConnectionError:
            # Return an error
            return render_template('dataunavailable.html')
        # If API responded, call the function
        return f()

    # Return the wrapper
    return wrapper


def requires_auth(permission=None):
    """
    Decorator which checks if the user is logged in and has the requested permission, and give the user to the function
    """

    # Define the decorator
    def decorator(f):
        # Define the decorated function
        def decorated():
            # Save the token from request's arguments
            token = request.args.get('token')
            # If the token isn't empty
            if token:
                # Send a request to know who's the user and save the response
                response = requests.get(f"{api_address}/tokens", data=json.dumps({"token": token}))
                # If the response is ok
                if response.status_code == 200:
                    # Save the user from the response
                    user = response.json()
                    # If permission isn't None
                    if permission:
                        # Try to test all the conditions
                        admin_perm = permission == 'admin' and user['permission'] == 'admin'
                        manager_perm = permission == 'manager' and user['permission'] in ['admin', 'manager']
                        investor_perm = permission == 'investor' and user['permission'] in ['admin', 'manager', 'investor']
                        # If user doesn't meet the conditions
                        if not (admin_perm or manager_perm or investor_perm):
                            # Return an error
                            return message("Vous n'avez pas la permission d'accéder ou de modifier ce contenu.", user['permission'], token)
                    # Add the token to user information
                    user['token'] = token
                    # Return the result of the function and give the user to the function
                    return f(user=user)
            # Send an error if the user isn't logged in or if his token is bad
            return message("Vous n'êtes pas authentifié dans l'application. Rendez-vous sur l'espace de connexion.", '', '')
        # Return the decorated function
        return decorated
    # Return the decorator
    return decorator


@app.route('/', endpoint='index')
@requires_api
def index():
    """
    Shows the main page
    """

    token = None
    connected = ""

    # If the URL contains the token
    if "token" in request.args:
        # Get the token from the request and save it
        token = request.args.get('token')
        # Send a request to know who's the user and save the response
        response = requests.get(f"{api_address}/tokens", data=json.dumps({"token": token}))
        # If the API responded ok
        if response.status_code == 200:
            # Set the variable connected to the permission of the user
            connected = response.json()['permission']
    # Send a request to get the pressings and save it
    response = requests.get(f"{api_address}/pressings")
    # Save the pressings from the response
    pressings = response.json()
    # Get the current pressing
    current = pressings[len(pressings)-1]
    # Set values to 0
    total_juice = 0
    total_apples = 0
    # For every pressing in pressings
    for pressing in pressings:
        # Add the juice of the pressing to total juice
        total_juice += pressing[1]
        # Add the apples of the pressing to total apples
        total_apples += pressing[2]
    # Calculate the juice per apples
    total_juice_per_apples = round(total_juice/total_apples, 2) if total_juice and total_apples else "Impossible de calculer "
    # Delete the current pressing from the pressings
    pressings.pop()
    # Reverse the pressings
    pressings.reverse()
    # Render the template
    return render_template('index.html', # The template
                           current_number=current[0], # The number of the current pressing
                           current_juice=current[1], # The produced juice of the current pressing
                           current_apples=current[2], # The apples used in the current pressing
                           current_juice_per_apples=current[3], # The juice per apples of the current pressing
                           total_juice=total_juice, # All the produced juice
                           total_apples=total_apples, # All the used apples
                           total_juice_per_apples=total_juice_per_apples, # The juice per apples of all the pressings
                           last_pressings=pressings, # A list of tuples (last pressings)
                           connected=connected, # If the user is connected, this is his permission
                           token=token) # If the user is connected, this is his token


@app.route('/login', methods=["GET"])
def get_login():
    """
    Shows the login page
    """

    # Return the template
    return render_template('login.html', address=address)


@app.route('/login', methods=["POST"], endpoint='post_login')
@requires_api
def post_login():
    """
    This isn't a page. This code authenticates the user and redirects him to the page of his permission
    """

    # Save the username and the password of the user from the form
    username = request.form['username']
    password = request.form['password']
    # Send a request to get a token and the permission of the user and save it
    response = requests.get(f"{api_address}/users", data=json.dumps({"username": username, "password": password}))
    # If the response is ok
    if response.status_code == 200:
        # Save the permission of the user
        permission = response.json()['permission']
        # If the user is an admin
        if permission == 'admin':
            # Redirect him to the admin page
            return redirect(f"{address}/admin?token={response.json()['token']}")
        # If the user is a manager
        elif permission == 'manager':
            # Redirect him to the manager page
            return redirect(f"{address}/manager?token={response.json()['token']}")
        # If the user is an investor
        elif permission == 'investor':
            # Redirect him to the investor page
            return redirect(f"{address}/investor?token={response.json()['token']}")
        # If the permission of the user is unknown
        else:
            # Send an error
            return message(f"Votre permission n'a pas été reconnue ({response.status_code} {response.json()['detail']}).", '', 'null')
    # If the user can't log in
    else:
        # Return an error
        return message(f"Vous ne pouvez pas vous connecter ({response.status_code} {response.json()['detail']}).", '', 'null')


@app.route('/manager', endpoint='manager')
@requires_api
@requires_auth('manager')
def manager(user):
    # Save the number of pressings from a request to the api
    nb_pressings = len(requests.get(f"{api_address}/pressings").json())
    # Save the number of apples used, invested and juice produced
    response = requests.get(f'{api_address}/apples')
    # Render the template
    return render_template('manager.html', api_address=api_address, used_apples=response.json()['used'], invested_apples=response.json()['invested'], produced_juice=response.json()['juice'], nb_pressings=nb_pressings, token=user['token'])


@app.route('/admin', endpoint='admin')
@requires_api
@requires_auth('admin')
def admin(user):
    """
    Shows the admin panel to users who have permission
    """

    # Render the admin page
    return render_template('admin.html', token=user['token'])


@app.route('/users', methods=["POST"], endpoint='add_remove_user')
@requires_api
@requires_auth('admin')
def add_remove_user(user):
    """
    Responds to the request from an admin form and adds or deletes an user
    """

    # If the form is the 'add' form
    if request.args.get('action') == "add":
        # Save the username, the password and the permission from the form
        target_username = request.form['username']
        target_password = request.form['password']
        target_permission = request.form['permission']
        # Create a variable which contains the information to send
        data = {"username": target_username, "password": target_password, "permission": target_permission}
        # Send a request with the data and save the response
        response = requests.post(f"{api_address}/users", data=json.dumps(data))
        # If the api answered 200
        if response.status_code == 200:
            # Return a confirmation
            return message("Vous avez bien créé l'utilisateur.", 'admin', user['token'])
        # If the api answered another status code
        else:
            # Return an error
            return message(f"L'utilisateur n'a pas pu être créé ({response.status_code} {response.json()['detail']}).", 'admin', user['username'])

    # If the form is the 'delete' form
    elif request.args.get('action') == "delete":
        # If the user doesn't try to delete his account
        if not user['username'] == request.form['username']:
            # Send a request to delete the user and save the response
            response = requests.delete(f"{api_address}/users", data=json.dumps({"username": request.form['username']}))
            # If the api answered 200
            if response.status_code == 200:
                # Return a confirmation
                return message("Vous avez bien supprimé l'utilisateur.", 'admin', user['token'])
            # If the api answered another status code
            else:
                # Return an error with the status code and detail
                return message(f"L'utilisateur n'a pas pu être supprimé ({response.status_code} {response.json()['detail']}).", 'admin', user['token'])
        # If the user tries to delete his account
        else:
            # Return an error
            return message(f"Par mesure de sécurité, vous ne pouvez pas supprimer votre compte.", 'admin', user['token'])


@app.route('/pressings', methods=["POST"], endpoint='add_edit_pressing')
@requires_api
@requires_auth('manager')
def add_edit_pressing(user):
    # If the user used the add form
    if request.args.get('action') == 'add':
        # Send a request to the API to add the pressing
        response = requests.post(f"{api_address}/pressings", data=json.dumps({"added_juice": request.form['juice'], "added_apples": request.form['apples']}))
        # If the response is ok
        if response.status_code == 200:
            # Return a confirmation
            return message("Vous avez bien créé une nouvelle pressée !", 'manager', user['token'])
        # If the response isn't ok
        else:
            # Send an error
            return message(f"Une erreur s'est produite lors de la création de la pressée ({response.status_code} {response.json()['detail']}).", 'manager', user['token'])
    # If the user used the edit form
    if request.args.get('action') == 'edit':
        # Save values from the form
        number = int(request.form['number'])
        added_juice = int(request.form['added_juice'])
        added_apples = int(request.form['added_apples'])
        # Send a request to the API to edit the pressing and save the response
        response = requests.post(f"{api_address}/pressings", data=json.dumps({"number": number, "added_juice": added_juice, "added_apples": added_apples}))
        # If the response is ok
        if response.status_code == 200:
            # Return a confirmation
            return message("Vous avez bien modifié la pressée !", 'manager', user['token'])
        # If the response isn't ok
        else:
            # Return an error
            return message(f"Une erreur s'est produite lors de l'ajout de valeurs ({response.status_code} {response.json()['detail']}).", 'manager', user['token'])


@app.route('/investor', methods=["GET"], endpoint='investo')
@requires_api
@requires_auth('investor')
def investor(user):
    # If the user is an admin or a manager
    if user['permission'] == 'admin' or user['permission'] == 'manager':
        # Send a request to get the investments
        investments = requests.get(f'{api_address}/investments', data=json.dumps({})).json()
        # Send a request to get his investment and save the response
        response = requests.get(f'{api_address}/investments', data=json.dumps({"username": user['username']}))
        apples = None
        brings = None
        if response.status_code == 200:
            apples = response.json()['apples']
            brings = response.json()['brings']
        # Render the template with response information
        return render_template('investor.html', investments=investments, permission=user['permission'], apples=apples, brings=brings, token=user['token'])
    # If the user is an investor
    elif user['permission'] == 'investor':
        # Send a request to get his investment and save the response
        response = requests.get(f'{api_address}/investments', data=json.dumps({"username": user['username']}))
        # If the response is ok
        if response.status_code == 200:
            # Save the apples and the user income
            apples = response.json()['apples']
            brings = response.json()['brings']
            # Render the template with response information
            return render_template('investor.html', permission=user['permission'], apples=apples, brings=brings, token=user['token'])
        # If the response isn't ok
        else:
            # Return an error
            return message("Votre investissement n'existe pas encore. Contactez le propriétaire de l'événement.", 'investor', user['token'])


@app.route('/investments', methods=["POST"], endpoint='add_edit_delete_investment')
@requires_api
@requires_auth('manager')
def add_edit_delete_investment(user):
    # If the user used the add/edit form
    if request.args.get('action') == 'add':
        # Send a request to the API to add an investment
        response = requests.post(f'{api_address}/investments', data=json.dumps({"username": request.form['username'], "apples": request.form['apples']}))
        # If the response is ok
        if response.status_code == 200:
            # Send a confirmation
            return message("L'investissement a bien été effectué", 'investor', user['token'])
        # If the response isn't ok
        else:
            # Return an error
            return message(f"Une erreur s'est produite pendant l'investissement ({response.status_code} {response.json()['detail']})", 'investor', user['token'])
    # If the user used the delete form
    elif request.args.get('action') == 'delete':
        # Send a request to the API and save the response
        response = requests.delete(f'{api_address}/investments', data=json.dumps({"username": request.form['username']}))
        # If the response is ok
        if response.status_code == 200:
            # Return a confirmation
            return message("Vous avez bien retiré l'investissement.", 'investor', user['token'])
        # If the response isn't ok
        else:
            # Send an error
            return message(f"L'investissement n'a pas pu être retiré ({response.status_code} {response.json()['detail']})", 'investor', user['token'])

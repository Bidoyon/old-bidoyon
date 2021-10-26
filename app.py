from flask import Flask, render_template, request, redirect

import requests
import json

app = Flask(__name__)
address = "https://jus-de-pomme-web.herokuapp.com"
api_address = "https://jus-de-pomme-api.herokuapp.com"


def message(text, panel, token):
    return render_template('message.html', text=text, address=address, panel=panel, token=token)


@app.route('/')
def index():

    response = requests.get(f"{api_address}/pressings")

    pressings = response.json()

    current = pressings[len(pressings)-1]

    total_juice = 0
    total_apples = 0

    for pressing in pressings:
        total_juice += pressing[1]
        total_apples += pressing[2]

    total_juice_per_apples = total_juice/total_apples if total_juice and total_apples else "Impossible de calculer "

    pressings.pop()

    pressings.reverse()

    return render_template('index.html',
                           current_number=current[0],
                           current_juice=current[1],
                           current_apples=current[2],
                           current_juice_per_apples=current[3],
                           total_juice=total_juice,
                           total_apples=total_apples,
                           total_juice_per_apples=total_juice_per_apples,
                           last_pressings=pressings)


@app.route('/login', methods=["GET"])
def get_login():
    return render_template('login.html', address=address)


@app.route('/login', methods=["POST"])
def post_login():

    username = request.form['username']
    password = request.form['password']

    response = requests.get(f"{api_address}/users", data=json.dumps({"username": username, "password": password}))

    if response.status_code == 200:

        permission = response.json()['permission']

        if permission == 'admin':

            return redirect(f"{address}/admin?token={response.json()['token']}")

        elif permission == 'manager':

            return redirect(f"{address}/manager?token={response.json()['token']}")

    return "No you don't"


@app.route('/manager')
def manager():
    token = request.args.get('token')

    response = requests.get(f"{api_address}/tokens", data=json.dumps({"token": token}))

    if response.status_code == 200 and (response.json()['permission'] == 'manager' or response.json()['permission'] == 'admin'):

        nb_pressings = len(requests.get(f"{api_address}/pressings").json())

        return render_template('manager.html', nb_pressings=nb_pressings, token=token)

    return "NO YOU DON'T"


@app.route('/admin')
def admin():

    token = request.args.get('token')

    response = requests.get(f"{api_address}/tokens", data=json.dumps({"token": token}))

    if response.status_code == 200 and response.json()['permission'] == 'admin':

        return render_template('admin.html', token=token)

    return "NO YOU DON'T"


@app.route('/users', methods=["POST"])
def add_remove_user():

    token = request.args.get('token')

    response = requests.get(f"{api_address}/tokens", data=json.dumps({"token": token}))

    if response.status_code == 200 and response.json()['permission'] == 'admin':

        if request.args.get('action') == "add":

            print(request.form['permission'])

            response = requests.post(f"{api_address}/users", data=json.dumps({"username": request.form['username'], "password": request.form['password'], "permission": request.form['permission']}))

            if response.status_code == 200:

                return message("Vous avez bien créé l'utilisateur.", 'admin', token)

            else:

                return message(f"L'utilisateur n'a pas pu être créé ({response.status_code} {response.reason}).", 'admin', token)

        elif request.args.get('action') == "delete":

            response = requests.delete(f"{api_address}/users", data=json.dumps({"username": request.form['username']}))

            if response.status_code == 200:

                return message("Vous avez bien supprimé l'utilisateur.", 'admin', token)

            else:

                return message(f"L'utilisateur n'a pas pu être supprimé ({response.status_code} {response.reason}).", 'admin', token)


@app.route('/pressings', methods=["POST"])
def add_edit_pressing():

    token = request.args.get('token')

    response = requests.get(f"{api_address}/tokens", data=json.dumps({"token": token}))

    if response.status_code == 200 and (response.json()['permission'] == 'manager' or response.json()['permission'] == 'admin'):

        if request.args.get('action') == 'add':

            response = requests.post(f"{api_address}/pressings", data=json.dumps({"added_juice": request.form['juice'], "added_apples": request.form['apples']}))

            if response.status_code == 200:

                return message("Vous avez bien créé une nouvelle pressée !", 'manager', token)

        if request.args.get('action') == 'edit':

            number = int(request.form['number'])
            added_juice = int(request.form['added_juice'])
            added_apples = int(request.form['added_apples'])

            response = requests.post(f"{api_address}/pressings", data=json.dumps({"number": number, "added_juice": added_juice, "added_apples": added_apples}))

            if response.status_code == 200:

                return message("Vous avez bien modifié la pressée !", 'manager', token)

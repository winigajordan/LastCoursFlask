from inspect import classify_class_attrs
import os
from socket import if_nameindex
from weakref import ref
from flask import Flask, redirect, url_for, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#Importation des formulaires
from forms import LoginForm, AddUserForm, DeleteUserForm, RegisterForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "TheCustomer"

# ----------------- config de la base de donnée -------------------------
basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#initialisation de l base de donnée
db = SQLAlchemy(app)

#activer les migration avec la base de donnée
Migrate(app, db)

# ----------------- fin de la config de la base de donnée -------------------------



# ----------------- creation des models -------------------------
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    nom = db.Column(db.String(50), nullable = False)
    prenom = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    #nouvelle colonne
    login = db.Column(db.String(50), nullable=True)
    password = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer, nullable = False)



    #constructeur
    def __init__(self, nom, prenom, age, email, password) :
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.email = email
        self.password = password

    #Methode toString
    
    def __repr__(self):
        return self.email

# ----------------- fin creation des models -------------------------


# ----------------- creation des vues -------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return  render_template("home.html")



@app.route("/connexion" , methods = ["GET","POST"])
def connexion():
    form = LoginForm()
    if form.validate_on_submit():
        log = form.login.data
        pwd = form.password.data
        user = User.query.filter_by(login = log, password = pwd).first()
        if user != None:
            session["userName"] = f"{user.nom} {user.prenom}"
            return render_template("home.html")
        else:
            flash("Login ou mot de passe incorrect")

    return render_template("connexion.html", form = form)


@app.route("/logout")
def logout():
    session.pop("userName", None)
    return redirect(url_for("index"))



@app.route("/register", methods = ["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        nom = form.nom.data
        prenom = form.prenom.data
        age = form.age.data
        email = form.email.data
        login = form.login.data
        password1 = form.password1.data
        password2 = form.password2.data
        if password1 != password2:
            flash("Les mots de passes sont different")
        else:
            user = User.query.filter_by(login=login).first()
            if user != None:
                flash(f"Le login : {login} existe déjà")
            else:
                newUser = User(nom, prenom, age, email, password1)
                newUser.login = login
                db.session.add(newUser)
                db.session.commit()
                return redirect(url_for("connexion"))

    return render_template("register.html", form=form   )

@app.route("/edit/<int:id>", methods = ["GET","POST"])
@app.route("/add", methods = ["GET","POST"], defaults = {"id":None})
def add_user(id):
    addform = AddUserForm()
    if addform.validate_on_submit():
        #print("Ok")
        nom = addform.nom.data
        prenom = addform.prenom.data
        age = addform.age.data
        email = addform.email.data
        password = addform.password.data
        newUser = User(nom, prenom, age, email, password)

        if id!=None:
            newUser = User.query.get(id)
            newUser.nom = nom
            newUser.prenom = prenom
            newUser.age = age
            newUser.email = email
            newUser.password = password

        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('list_user'))

    if id!=None:
        user = User.query.get(id)
        if not user :
            return redirect(url_for("list_user"))
        addform.nom.data = user.nom
        addform.prenom.data = user.prenom
        addform.age.data = user.age
        addform.email.data = user.email
        addform.password.data = user.password

    return render_template("add.html", form = addform, userId = id)


@app.route("/list")
def list_user():
    users = User.query.all()
    return render_template("list.html", users = users)


@app.route("/delete/<int:id>")
@app.route("/delete", methods = ["GET","POST"], defaults={"id": None})
def delete_user(id):
    if id:
        db.session.delete(User.query.get(id))
        db.session.commit()
        return redirect(url_for('list_user'))

    form = DeleteUserForm()
    if form.validate_on_submit():
        id = form.id.data
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('list_user'))
        else:
            flash("Utilisateur non trouvé")


    return render_template("delete.html", form = form)




if __name__ == '__main__':
    app.run(debug=True)



"""
    if form.validate_on_submit():
        nom = form.nom.data
        prenom = form.prenom.data
        age = form.age.data
        email = form.email.data
        login = form.login.data
        password1 = form.password1.data
        password2 = form.password2.data
        if password1 != password2:
            flash("Les mots de passes sont different")
        else:
            user = User.query.filter_by(login = login).first()
            if user != None:
                flash(f"Ce login : {login} existe déjà")
            else :
                newUser = User(nom, prenom, age, email, password)
                newUser.login = login
                db.session.add(newUser)
                db.session.commit()
                return  redirect(url_for("connexion"))

"""
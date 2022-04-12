from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired

#-------------------- Cr&ation des formulaire --------------------
class LoginForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired()])
    password = PasswordField ("Password", validators=[DataRequired("Mot de passe obligatoire")])
    submit = SubmitField("Connexion")

class AddUserForm(FlaskForm):
    nom = StringField("Nom", validators=[DataRequired()])
    prenom = StringField("Prenom", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Ajout")

class DeleteUserForm(FlaskForm):
    id = IntegerField("User Id", validators=[DataRequired()])
    submit = SubmitField("Remove")

class RegisterForm(FlaskForm):
    nom = StringField("Nom", validators=[DataRequired()])
    prenom = StringField("Prenom", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    login = StringField("Login", validators=[DataRequired()])
    password1 = PasswordField("Mot de passe", validators=[DataRequired()])
    password2= PasswordField("Confirger mot de passe", validators=[DataRequired()])
    submit = SubmitField("Ajout")
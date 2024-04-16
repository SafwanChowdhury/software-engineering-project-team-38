from pickle import FALSE
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DateTimeField, IntegerField, SubmitField, EmailField, SelectField, FieldList, TextAreaField
from wtforms.validators import EqualTo, DataRequired, ValidationError, Length, Email, Regexp, NumberRange
from app import models
from datetime import date, datetime
import pycountry


class Login(FlaskForm):
    email = StringField("Enter email", validators=[DataRequired(), Length(max=60)])
    password = PasswordField("Enter password", validators=[DataRequired(), Length(max=60)])
    submit = SubmitField("Submit")


class Report(FlaskForm):
    issue = SelectField(choices=["Refund", "Problem with website", "Problem with registration", "Problem with login", "Other"])
    report = TextAreaField("Describe the issue:", validators=[DataRequired(), Length(max=150)])
    submit = SubmitField("Submit")


class Registration(FlaskForm):
        username = StringField("Enter username", validators=[DataRequired(), Length(max=60)], render_kw={"placeholder": "Full Name","style" : "width: 135px; font-size: 13px; font-family: Halyard Display; font-style: normal; font-weight: normal;"})
        email = StringField("Enter email", validators=[DataRequired(), Length(max=60), Email()], render_kw={"placeholder": "Email", "style" : "width: 292px; font-size: 13px; font-family: Halyard Display; font-style: normal; font-weight: normal;"})
        password_1 = PasswordField("Enter password", validators=[DataRequired(), Length(min=8,max=60)], render_kw={"placeholder": "Password", "style" : "width: 292px; font-size: 13px; font-family: Halyard Display; font-style: normal; font-weight: normal;"})
        password_2 = PasswordField("Confirm password", validators=[DataRequired(), Length(min=8,max=60), EqualTo("password_1", message="Passwords must match!")], render_kw={"placeholder": "Confirm Password","style" : "width: 292px; font-size: 13px; font-family: Halyard Display; font-style: normal; font-weight: normal;"})
        submit = SubmitField("Submit", render_kw={"placeholder": "SIGN UP"})
        age = StringField("Enter Age", validators=[DataRequired()], render_kw={"placeholder": "Age", "style" : "width: 292px; font-size: 13px; font-family: Halyard Display; font-style: normal; font-weight: normal;"})
        
        # function that validates email adress upon registration
        def validate_email(self, email):     
            user_object = models.User.query.filter_by(email=email.data).first()
            if user_object: #if user is already registered don"t allow them to register again
                raise ValidationError("This email address is already registered!")

        #function that validates the password when registering a new user
        def validate_password_1(self, password_1):
            count_numbers = 0
            count_lowercase = 0
            count_uppercase = 0
            
            #if at least one of these characters in here are in PW, error
            chars_number = "1234567890" 
            chars_uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            chars_lowercase = "abcdefghijklmnopqrstuvwxyz"

            for char in self.password_1.data:
                if char in chars_number:
                    count_numbers+=1
                if char in chars_lowercase:
                    count_lowercase+=1
                if char in chars_uppercase:
                    count_uppercase+=1

            if count_numbers == 0:
                    raise ValidationError(f"Password must have at least 1 number")
            if count_lowercase == 0:
                    raise ValidationError(f"Password must have at least 1 lowercase letter")
            if count_uppercase == 0:
                    raise ValidationError(f"Password must have at least 1 uppercase letter")


class Booking(FlaskForm):
    location = StringField("")
    hours = StringField("")
    submit = SubmitField("Submit")
    

class Payment(FlaskForm):
    
    #card details
    name = StringField("Enter name", validators=[DataRequired(message = "Enter your name please"), Length(max=60)])
    card_number = StringField("Enter card number", validators=[DataRequired(), Length(min=14, max=20)])
    cvv = StringField("Enter cvv", validators=[DataRequired() , Length(min=3, max=4)],render_kw={"placeholder": "123"})
    expiry_date = DateTimeField("Enter expiry date (mm/YYYY)", validators=[DataRequired()], format="%m/%Y",render_kw={"placeholder": "mm/YYYY"})
    submit = SubmitField("Submit")

    #billing details
    address_line_1 = StringField("Address line 1", validators=[DataRequired(), Length(max=60)])
    address_line_2 = StringField("Address line 2", validators=[Length(max=60)])
    city = StringField("City", validators=[DataRequired(), Length(max=60)])
    postcode = StringField("Postcode", validators=[DataRequired(), Length(min=6, max=7)])
    
    #united kingdom appears at the beginning of the country list
    country_list = [("United Kingdom")]
    for c in pycountry.countries:
        country_list.append(c.name)
    
    country = SelectField("Select country", choices = country_list)

    # Checks
    def validate_name(self, name):
        excluded_chars = "*?!'^+%&/()=}][{$#£1234567890"
        for char in self.name.data:
            if char in excluded_chars:
                raise ValidationError(f"Character {char} is not allowed in name.")
    
    def validate_expiry_date(self, expiry_date):
        if (datetime.today() - expiry_date.data).days > 0:
            raise ValidationError("Expiry date is not valid")

    def validate_card_number(self, card_number):
        chars = "1234567890"
        for char in self.card_number.data:
            if not char in chars:
                raise ValidationError(f"Character {char} is not allowed in card number.")
    
    def validate_cvv(self, cvv):
        chars = "1234567890"
        for char in self.cvv.data:
            if not char in chars:
                raise ValidationError(f"Character {char} is not allowed in cvv.")


class Guest_Payment(FlaskForm):
    def luhns(card_number):
        
        #check if card number is numeric
        if not card_number.isnumeric():
            return -1
        else: 
            card_number = int(card_number)

        digits = [int(x) for x in str(card_number)]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(int(x) for x in str(d*2))
        return checksum % 10

    email = StringField("Enter email", validators=[DataRequired(), Length(max=60), Email()])
    #card details
    name = StringField("Enter name", validators=[DataRequired(message = "Enter your name please"), Length(max=60)])
    card_number = StringField("Enter card number", validators=[DataRequired(), Length(min=14, max=20)])
    cvv = StringField("Enter cvv", validators=[DataRequired() , Length(min=3, max=4)],render_kw={"placeholder": "123"})
    expiry_date = DateTimeField("Enter expiry date (mm/YYYY)", validators=[DataRequired()], format="%m/%Y",render_kw={"placeholder": "mm/YYYY"})
    submit = SubmitField("Submit")
    location = StringField("")
    hours = StringField("")

    #billing details
    address_line_1 = StringField("Address line 1", validators=[DataRequired(), Length(max=60)])
    address_line_2 = StringField("Address line 2", validators=[Length(max=60)])
    city = StringField("City", validators=[DataRequired(), Length(max=60)])
    postcode = StringField("Postcode", validators=[DataRequired(), Length(min=6, max=7)])
    
    #hardcoded to start with united_kingdom
    country_list = [("United Kingdom")]
    for c in pycountry.countries:
        country_list.append(c.name)
    
    country = SelectField("Select country", choices = country_list)

    # Checks
    def validate_name(self, name):
        excluded_chars = "*?!'^+%&/()=}][{$#£1234567890"
        for char in self.name.data:
            if char in excluded_chars:
                raise ValidationError(f"Character {char} is not allowed in name.")
    
    def validate_expiry_date(self, expiry_date):
        if (datetime.today() - expiry_date.data).days > 0:
            raise ValidationError("Expiry date is not valid")


    def validate_card_number(self, card_number):
        chars = "1234567890"
        for char in self.card_number.data:
            if not char in chars:
                raise ValidationError(f"Character {char} is not allowed in card number.")
    
    def validate_cvv(self, cvv):
        chars = "1234567890"
        for char in self.cvv.data:
            if not char in chars:
                raise ValidationError(f"Character {char} is not allowed in cvv.")
                    
    
class Prices(FlaskForm):
    hour_price = StringField("Enter a price", validators=[DataRequired(), Length(max= 60), Regexp("\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})")])
    four_hour_price= StringField("Enter a price", validators=[DataRequired(), Length(max=60)])
    day_price = StringField("Enter a price", validators=[DataRequired(), Length(max=60)])
    week_price = StringField("Enter a price", validators=[DataRequired(), Length(max=60)])
    submit = SubmitField("Submit")

    # def valid_float(self, price):
    #     count = 0
    #     for i in range(len(price)):
    #         if price[i] == ".":
    #             count+=1
    #             if count > 1:
    #                 raise ValidationError("Invalid Price entered. Should follow the format - 0.00")

         
class AddScooter(FlaskForm):
    location = SelectField(u"Select Location to add Scooter: ", choices = [(1,"Trinity Centre"), (2,"Train Station"), (3,"Merrion Centre"), (4,"LRI Hospital"), (5,"UoL Edge")])
    submit = SubmitField("Add Scooter")


class EditScooter(FlaskForm):
    location = SelectField(u"Select new location for Scooter: ", choices = [(1,"Trinity Centre"), (2,"Train Station"), (3,"Merrion Centre"), (4,"LRI Hospital"), (5,"UoL Edge")])
    in_use = SelectField(u"Select whether the scooter is currently in use: ", choices= [(0,"No"), (1,"Yes")])
    submit = SubmitField("Apply Changes")

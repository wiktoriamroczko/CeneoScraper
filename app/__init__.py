#import bibliotek
from flask import Flask

#utworzenie obiektu (instancji) klasy flask reprezentującego aplikację
app = Flask(__name__)

#import widoków/routingów z aplikiacji
from app import views

#uruchomienie aplikacji
if __name__=='__main__':
    app.run(debug=True)
# AnimalShelterMS
This project is a DBMS for an Animal Shelter which aims to manage data about medical records, adoptions and daily needs of animals and the various employees and vets associated with the Shelter.
# How to use
0. Download the code and install all the requirements.
1. Start a MySQL server and run Make_database.sql in the server to make all the required tables.
2. In order to connect flask to the database, The following line needs to be edited:<br>
      `app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:password@localhost/AnimalShelterMS'
      `
3. Run python runserver.py to serve the flask app.
4. The website will be on http://localhost:5555/ . username: admin, password:admin

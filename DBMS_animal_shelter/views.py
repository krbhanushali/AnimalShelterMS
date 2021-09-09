"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from DBMS_animal_shelter import app
from sqlalchemy import or_
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import aliased
db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect = True)

Person = Base.classes.person
Employee = Base.classes.employee
Vet = Base.classes.vet
Animal = Base.classes.animal
MedicalRecords = Base.classes.medicalrecords
Tasks = Base.classes.dailytasks
Adoptions = Base.classes.adoptions
# use Base.classes.<table name> for the class
@app.route('/login', methods = ['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username']!='admin' or request.form['password']!='admin':
            error = 'Invalid Credentials. Try again.'
        else:
            return redirect(url_for('dashboard'))
    login = True
    return render_template(
    'login.html',
    title = 'Login',
    year=datetime.now().year,
    error = error
    )

@app.route('/') #check if logged in and then manage
@app.route('/home', methods=['POST','GET'])
def home():
    """Renders the home page."""

    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year
    )

@app.route('/dashboard',methods=['POST','GET'])
def dashboard():
    return render_template(
        'dashboard.html',
        title = 'Dashboard',
        year=datetime.now().year
    )

@app.route('/animals',methods=['POST','GET'])
@app.route('/animals/<int:page>', methods=['POST','GET'])
def animals(page = 1):
    per_page = 20
    query = db.session.query(Animal).paginate(page, per_page, error_out=False)
    error = None
    if request.method=='POST':
        input_query = request.form['query']
        result =  db.session.query(Animal).filter(Animal.Name==input_query)
        if len(input_query)==0 or input_query == 'all':
            result = query
        return render_template(
            "animals.html",
            title = 'Animals',
            year=datetime.now().year,
            error = error,
            posts = result
        )
    return render_template(
        "animals.html",
        title = 'Animals',
        year=datetime.now().year,
        error = error,
        posts = query
    )

@app.route('/vets',methods=['POST','GET'])
@app.route('/vets/<int:page>',methods=['POST','GET'])
def vets(page = 1):
    query = db.session.query(Vet)
    print(inspect(query))
    per_page = 20
    query = db.session.query(Vet)\
        .join(Person, Person.PersonID ==Vet.PersonID)\
        .add_columns(Person.FirstName,
                     Person.LastName,
                     Person.Phone,
                     Vet.VetID,
                     Vet.OfficeContact) \
        .paginate(page, per_page, error_out=False)

    error = None
    if request.method=='POST':
        input_query = request.form['query']
        result =  db.session.query(Vet)\
            .join(Person, Person.PersonID ==Vet.PersonID)\
            .add_columns(Person.FirstName,
                         Person.LastName,
                         Person.Phone,
                         Vet.RegNo,
                         Vet.OfficeContact,
                         Vet.VetID) \
            .filter(or_((Person.FirstName==input_query),(Person.LastName==input_query)))\
            .paginate(page, per_page, error_out=False)
        if len(input_query)==0 or input_query == 'all':
            result = query
        return render_template(
            "vets.html",
            title = 'Vets',
            year=datetime.now().year,
            error = error,
            posts = result
        )
    return render_template(
        "vets.html",
        title = 'Vets',
        year=datetime.now().year,
        error = error,
        posts = query
    )

@app.route('/employees',methods=['POST','GET'])
@app.route('/employees/<int:page>', methods=['POST','GET'])
def employees(page=1):
    per_page = 20
    query = db.session.query(Employee)\
        .join(Person, Person.PersonID ==Employee.PersonID)\
        .add_columns(Person.FirstName,
                     Person.LastName,
                     Person.Phone,
                     Employee.WorkerID,
                     Employee.Salary,
                     Employee.CompanyEmail) \
        .paginate(page, per_page, error_out=False)

    error = None
    if request.method=='POST':
        input_query = request.form['query']
        result =  db.session.query(Employee)\
            .join(Person, Person.PersonID ==Employee.PersonID)\
            .add_columns(Person.FirstName,
                         Person.LastName,
                         Person.Phone,
                         Employee.WorkerID,
                         Employee.Salary,
                         Employee.CompanyEmail) \
            .filter(or_((Person.FirstName==input_query),(Person.LastName==input_query)))\
            .paginate(page, per_page, error_out=False)
        if len(input_query)==0 or input_query == 'all':
            result = query
        return render_template(
            "employees.html",
            title = 'Employees',
            year=datetime.now().year,
            error = error,
            posts = result
        )
    return render_template(
        "employees.html",
        title = 'Employees',
        year=datetime.now().year,
        error = error,
        posts = query
    )

@app.route('/people', methods= ['POST', 'GET'])
@app.route('/people/<int:page>', methods=['POST', 'GET'])
def people(page = 1):
    per_page = 20
    query = db.session.query(Person).paginate(page, per_page, error_out=False)
    error = None
    if request.method=='POST':
        input_query = request.form['query']
        result =  db.session.query(Person).filter(or_((Person.FirstName==input_query),(Person.LastName==input_query)))\
        .paginate(page, per_page, error_out=False)
        if len(input_query)==0 or input_query == 'all':
            result = query
        return render_template(
            "people.html",
            title = 'People',
            year=datetime.now().year,
            error = error,
            posts = result
        )
    return render_template(
        "people.html",
        title = 'People',
        year=datetime.now().year,
        error = error,
        posts = query
    )

@app.route('/tasks', methods= ['POST', 'GET'])
@app.route('/tasks/<int:page>', methods=['POST', 'GET'])
def tasks(page = 1):
    per_page = 20
    query = db.session.query(Tasks)\
            .join(Employee, Employee.WorkerID == Tasks.WorkerID)\
            .join(Animal, Animal.AnimalID == Tasks.AnimalID)\
            .join(Person, Person.PersonID == Employee.PersonID)\
            .add_columns(Animal.Name, Tasks.Task, Tasks.Description, Person.FirstName, Person.LastName)\
            .paginate(page, per_page, error_out=False)

    error = None
    if request.method=='POST':
        input_query = request.form['query']
        result = db.session.query(Tasks)\
                .join(Employee, Employee.WorkerID == Tasks.WorkerID)\
                .join(Animal, Animal.AnimalID == Tasks.AnimalID)\
                .join(Person, Person.PersonID == Employee.PersonID)\
                .add_columns(Animal.Name, Tasks.Task, Tasks.Description, Person.FirstName, Person.LastName)\
                .filter(or_((Person.FirstName==input_query),(Person.LastName==input_query),(Animal.Name==input_query)))\
                .paginate(page, per_page, error_out=False)
        if len(input_query)==0 or input_query == 'all':
            result = query
        return render_template(
            "tasks.html",
            title = 'Tasks',
            year=datetime.now().year,
            error = error,
            posts = result
        )
    return render_template(
        "tasks.html",
        title = 'Tasks',
        year=datetime.now().year,
        error = error,
        posts = query
    )

@app.route('/adoptions', methods= ['POST', 'GET'])
@app.route('/adoptions/<int:page>', methods=['POST', 'GET'])
def adoptions(page = 1):
    per_page = 20
    WorkerDetails = aliased(Person)
    Adopter = aliased(Person)
    query = db.session.query(Adoptions)\
            .join(Employee, Employee.WorkerID == Adoptions.Overseer)\
            .join(Animal, Animal.AnimalID == Adoptions.AnimalID)\
            .join(Adopter, Adopter.PersonID == Adoptions.PersonID)\
            .join(WorkerDetails, WorkerDetails.PersonID == Employee.PersonID)\
            .add_columns(Animal.Name,
                         Adopter.FirstName.label('Adopter_name_f'),
                         Adopter.LastName.label('Adopter_name_s'),
                         WorkerDetails.FirstName,
                         WorkerDetails.LastName,
                         Adoptions.AdoptionID,
                         Adoptions.DateOfAdoption)\
            .paginate(page, per_page, error_out=False)

    error = None
    if request.method=='POST':
        input_query = request.form['query']
        result = db.session.query(Adoptions)\
                .join(Employee, Employee.WorkerID == Adoptions.Overseer)\
                .join(Animal, Animal.AnimalID == Adoptions.AnimalID)\
                .join(Adopter, Adopter.PersonID == Adoptions.PersonID)\
                .join(WorkerDetails, WorkerDetails.PersonID == Employee.PersonID)\
                .add_columns(Animal.Name,
                             Adopter.FirstName.label('Adopter_name_f'),
                             Adopter.LastName.label('Adopter_name_s'),
                             WorkerDetails.FirstName,
                             WorkerDetails.LastName,
                             Adoptions.AdoptionID,
                             Adoptions.DateOfAdoption)\
                .filter(or_((WorkerDetails.FirstName==input_query),
                            (WorkerDetails.LastName==input_query),
                            (Animal.Name==input_query),
                            (Adopter.FirstName==input_query),
                            (Adopter.LastName==input_query)))\
                .paginate(page, per_page, error_out=False)

        if len(input_query)==0 or input_query == 'all':
            result = query

        return render_template(
            "adoptions.html",
            title = 'Adoptions',
            year=datetime.now().year,
            error = error,
            posts = result
        )
    return render_template(
        "adoptions.html",
        title = 'Adoptions',
        year=datetime.now().year,
        error = error,
        posts = query
    )

@app.route('/medicalrecords', methods= ['POST', 'GET'])
@app.route('/medicalrecords/<int:page>', methods=['POST', 'GET'])
def medicalrecords(page = 1):
    per_page = 20
    query = db.session.query(MedicalRecords)\
        .join(Animal, Animal.AnimalID ==MedicalRecords.AnimalID)\
        .join(Vet, Vet.VetID == MedicalRecords.VetID)\
        .join(Person, Vet.PersonID == Person.PersonID)\
        .add_columns(Person.FirstName,
                     Person.LastName,
                     Animal.Name,
                     MedicalRecords.Time,
                     MedicalRecords.TypeOfVisit,
                     MedicalRecords.Healthy,
                     MedicalRecords.RecordID) \
        .paginate(page, per_page, error_out=False)

    error = None
    if request.method=='POST':
        input_query = request.form['query']
        result =  db.session.query(MedicalRecords)\
                    .join(Animal, Animal.AnimalID ==MedicalRecords.AnimalID)\
                    .join(Vet, Vet.VetID == MedicalRecords.VetID)\
                    .join(Person, Vet.PersonID == Person.PersonID)\
                    .add_columns(Person.FirstName,
                         Person.LastName,
                         Animal.Name,
                         MedicalRecords.Time,
                         MedicalRecords.TypeOfVisit,
                         MedicalRecords.Healthy,
                         MedicalRecords.RecordID) \
                    .filter(or_((Person.FirstName==input_query),
                                (Person.LastName==input_query),
                                (Animal.Name==input_query)))\
                    .paginate(page, per_page, error_out=False)
        if len(input_query)==0 or input_query == 'all':
            result = query
        return render_template(
            "records.html",
            title = 'Medical Records',
            year=datetime.now().year,
            error = error,
            posts = result
        )
    return render_template(
        "records.html",
        title = 'Medical Records',
        year=datetime.now().year,
        error = error,
        posts = query
    )

@app.route('/animals/new', methods=['POST', 'GET'])
@app.route('/animals/new/<int:page>', methods=['POST', 'GET'])
def new_animal(page=1):
    per_page = 5
    query = db.session.query(Animal).paginate(page, per_page, error_out=False)
    error = None
    if request.method=='POST':
        name = request.form['name']
        DateOfBirth = request.form['dob']
        Gender = request.form['gender']
        Breed = request.form['breed']
        Weight = request.form['weight']
        Healthy = request.form['healthy']
        animal = Animal(Name = name,
                        DateOfBirth = DateOfBirth,
                        Gender = Gender,
                        Breed = Breed,
                        Weight = Weight,
                        Healthy = Healthy)

        db.session.add(animal)
        db.session.commit()
        return redirect(url_for('new_animal'))

    return render_template(
        "new_animal.html",
        title = 'New Animal',
        year=datetime.now().year,
        error = error,
        posts = query
    )

@app.route('/vets/new', methods=['POST', 'GET'])
@app.route('/vets/new/<int:page>', methods=['POST', 'GET'])
def new_vet(page = 1):
    per_page = 5
    query = db.session.query(Vet)\
        .join(Person, Person.PersonID ==Vet.PersonID)\
        .add_columns(Person.FirstName,
                     Person.LastName,
                     Person.Phone,
                     Vet.VetID,
                     Vet.OfficeContact) \
        .paginate(page, per_page, error_out=False)
    error = None
    if request.method=='POST':
        personID = request.form['pID']
        regNo = request.form['RegNo']
        contact = request.form['OfficePh']

        vet = Vet(PersonID = personID, OfficeContact = contact, RegNo = regNo)

        db.session.add(vet)
        db.session.commit()
        return redirect(url_for('new_vet'))

    return render_template(
        "new_vet.html",
        title = 'New Vet',
        year=datetime.now().year,
        error = error,
        posts = query
    )

@app.route('/employees/new', methods=['POST', 'GET'])
@app.route('/employees/new/<int:page>', methods=['POST', 'GET'])
def new_employee(page = 1):
    per_page = 5
    query = db.session.query(Employee)\
        .join(Person, Person.PersonID ==Employee.PersonID)\
        .add_columns(Person.FirstName,
                     Person.LastName,
                     Person.Phone,
                     Employee.WorkerID,
                     Employee.Salary,
                     Employee.CompanyEmail) \
        .paginate(page, per_page, error_out=False)
    error = None
    if request.method=='POST':
        personID = request.form['pID']
        seniorID = request.form['sID']
        salary = request.form['salary']
        companyEmail = request.form['compEmail']
        if len(seniorID)!=0:
            employee = Employee(PersonID = personID,SeniorID= seniorID,Salary= salary, CompanyEmail= companyEmail)
        else:
            employee = Employee(PersonID = personID,Salary= salary, CompanyEmail= companyEmail)
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('new_employee'))

    return render_template(
        "new_employee.html",
        title = 'New Employee',
        year=datetime.now().year,
        error = error,
        posts = query
    )

@app.route('/people/new', methods= ['POST', 'GET'])
@app.route('/people/new/<int:page>', methods=['POST', 'GET'])
def new_person(page = 1):
    per_page = 5
    query = db.session.query(Person).paginate(page, per_page, error_out=False)
    error = None
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        name_ = name.split(' ')
        if(len(name_)==1): first_name,last_name = name, ''
        else: first_name, last_name = name.split(' ')[0], name.split(' ')[-1]
        person = Person(Email = email,Phone= phone,Address= address, FirstName= first_name,LastName= last_name)
        db.session.add(person)
        db.session.commit()
        return redirect(url_for('new_person'))

    return render_template(
        "new_person.html",
        title = 'New Person',
        year=datetime.now().year,
        error = error,
        posts = query
    )

@app.route('/tasks/new', methods= ['POST', 'GET'])
@app.route('/tasks/new/<int:page>', methods=['POST', 'GET'])
def new_task(page = 1):
    per_page = 5
    query = db.session.query(Tasks)\
    .join(Employee, Employee.WorkerID == Tasks.WorkerID)\
    .join(Animal, Animal.AnimalID == Tasks.AnimalID)\
    .join(Person, Person.PersonID == Employee.PersonID)\
    .add_columns(Animal.Name, Tasks.Task, Tasks.Description, Person.FirstName, Person.LastName)\
    .paginate(page, per_page, error_out=False)

    error = None

    if request.method=='POST':
        workerID = request.form['wID']
        animalID = request.form['aID']
        taskDesc = request.form['task']
        task = Tasks(WorkerID = workerID, AnimalID = animalID, Description = taskDesc)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('new_task'))

    return render_template(
        "new_task.html",
        title = 'New Task',
        year=datetime.now().year,
        error = error,
        posts = query
    )

@app.route('/adoptions/new', methods= ['POST', 'GET'])
@app.route('/adoptions/new/<int:page>', methods=['POST', 'GET'])
def new_adoption(page = 1):
    per_page = 5
    WorkerDetails = aliased(Person)
    Adopter = aliased(Person)
    query = db.session.query(Adoptions)\
            .join(Employee, Employee.WorkerID == Adoptions.Overseer)\
            .join(Animal, Animal.AnimalID == Adoptions.AnimalID)\
            .join(Adopter, Adopter.PersonID == Adoptions.PersonID)\
            .join(WorkerDetails, WorkerDetails.PersonID == Employee.PersonID)\
            .add_columns(Animal.Name,
                         Adopter.FirstName.label('Adopter_name_f'),
                         Adopter.LastName.label('Adopter_name_s'),
                         WorkerDetails.FirstName,
                         WorkerDetails.LastName,
                         Adoptions.AdoptionID,
                         Adoptions.DateOfAdoption)\
            .paginate(page, per_page, error_out=False)
    error = None

    if request.method=='POST':
        workerID = request.form['wID']
        animalID = request.form['aID']
        adopter = request.form['pID']
        date = datetime.now()
        adoption = Adoptions(PersonID = adopter, AnimalID = animalID, Overseer = workerID, DateOfAdoption = date, AdoptionID=90)
        db.session.add(adoption)
        db.session.commit()
        return redirect(url_for('new_adoption'))

    return render_template(
        "new_adoption.html",
        title = 'New Adoption',
        year=datetime.now().year,
        error = error,
        posts = query
    )

@app.route('/medicalrecords/new', methods= ['POST', 'GET'])
@app.route('/medicalrecords/new/<int:page>', methods=['POST', 'GET'])
def new_record(page = 1):
    per_page = 5
    query = db.session.query(MedicalRecords)\
            .join(Animal, Animal.AnimalID ==MedicalRecords.AnimalID)\
            .join(Vet, Vet.VetID == MedicalRecords.VetID)\
            .join(Person, Vet.PersonID == Person.PersonID)\
            .add_columns(Person.FirstName,
                         Person.LastName,
                         Animal.Name,
                         MedicalRecords.Time,
                         MedicalRecords.TypeOfVisit,
                         MedicalRecords.Healthy,
                         MedicalRecords.RecordID) \
            .paginate(page, per_page, error_out=False)
    error = None
    if request.method=='POST':
        vetID = request.form['vID']
        animalID = request.form['aID']
        healthy = request.form['healthy']
        type = request.form['visitType']
        date = datetime.now()
        Comments = request.form['comment']
        record = MedicalRecords(VetID = vetID, AnimalID = animalID, Time = date, TypeOfVisit=type, Healthy=healthy, Comments=Comments, RecordID=100)
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('new_record'))

    return render_template(
        "new_record.html",
        title = 'New Record',
        year=datetime.now().year,
        error = error,
        posts = query
    )

@app.route('/animals/animal/<int:id>', methods=['POST','GET'])
def animal(id):
    return render_template('layout.html')

@app.route('/vets/vet/<int:id>',methods=['POST','GET'])
def vet(id):
    return render_template('layout.html')

@app.route('/employees/employee/<int:id>', methods=['POST','GET'])
def worker(id):
    query = db.session.query(Employee).filter_by(WorkerID=id)
    return render_template(
        'person.html',
        title= 'Profile',
        year= datetime.now().year,
        data = query[0]
    )

@app.route('/people/person/<int:id>', methods=['POST', 'GET'])
def person(id):
    query = db.session.query(Person).filter_by(PersonID=id)
    return render_template(
        'person.html',
        title= 'Profile',
        year=datetime.now().year,
        data = query[0]
    )

@app.route('/tasks/task/<int:id>', methods=['POST', 'GET'])
def task(id):
    query = db.session.query(Person).filter_by(PersonID=id)
    return render_template(
        'person.html',
        title= 'Profile',
        year=datetime.now().year,
        data = query[0]
    )

@app.route('/medicalrecords/record/<int:id>', methods=['POST', 'GET'])
def record(id):
    query = db.session.query(Person).filter_by(PersonID=id)
    return render_template(
        'person.html',
        title= 'Profile',
        year=datetime.now().year,
        data = query[0]
    )

@app.route('/adoptions/adoption/<int:id>', methods=['POST', 'GET'])
def adoption(id):
    query = db.session.query(Person).filter_by(PersonID=id)
    return render_template(
        'person.html',
        title= 'Profile',
        year=datetime.now().year,
        data = query[0]
    )

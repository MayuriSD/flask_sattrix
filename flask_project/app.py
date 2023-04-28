from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(200))
    company = db.Column(db.String(50))
    branch = db.Column(db.String(50))

    def __init__(self, first_name, last_name, company,branch ):

        self.first_name = first_name
        self.last_name = last_name
        self.company = company
        self.branch = branch

@app.route('/employee', methods=['POST'])
def create_emp():
    """
    This function will create new employee in database
    :return: employee
    """
    message = {
        'status': 404,
        'message': 'Something went wrong'
    }
    try:
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        company = request.json['company']
        branch = request.json['branch']
        emp = Employee(
            first_name,
            last_name,
            company,
            branch
        )
        db.session.add(emp)
        db.session.commit()
        message.update({
            "status": 201,
            "message": "User created successfully!!! ",
            })
    except:
        pass
    resp = jsonify(message)
    return resp


@app.route('/employee', methods=['GET'])
def get_all_emps():
    """
    This function will return all employoees in database

    """
    message = {
        'status': 404,
        'message': 'Something went wrong'
    }
    try:
        emps = Employee.query.all()
        result = []
        for emp in emps:
            emp_data = {}
            emp_data['id'] = emp.id
            emp_data['first_name'] = emp.first_name
            emp_data['last_name'] = emp.last_name
            emp_data['company'] = emp.company
            emp_data['branch'] = emp.branch
            result.append(emp_data)
        return jsonify(result)

    except:
        pass
    return jsonify(message)


@app.route('/employee/<int:id>', methods=['GET'])
def get_specific_emp(id):
    message = {
        'status': 404,
        'message': 'User not exists'
    }
    data = Employee.query.filter_by(id=id).first()
    if not data:
        return jsonify(message)

    emp_data={}
    emp_data['id'] = data.id
    emp_data['first_name'] = data.first_name
    emp_data['last_name'] = data.last_name
    emp_data['company'] = data.company
    emp_data['branch'] = data.branch
    message.update({
        'status': 200,
        'message': 'ALl records are fetched',
        'data': emp_data
    })
    return jsonify(message)


@app.route('/employee/<int:id>', methods=['PUT'])
def update_emp(id):
    """
    This function will update an existing employee

    """
    message = {
        'status': 404,
        'message': 'Emp not found'
    }
    try:
        new_first_name = request.json['first_name']
        new_last_name = request.json['last_name']
        new_comapny = request.json['company']
        new_branch = request.json['branch']
        try:
            current_emp = Employee.query.get_or_404(id)
        except:
            return jsonify(message)

        if new_first_name:
            current_emp.first_name = new_first_name
        if new_last_name:
            current_emp.last_name = new_last_name
        if new_comapny:
            current_emp.company = new_comapny
        if new_branch:
            current_emp.branch = new_branch

        db.session.commit()
        message.update({
            'status': 200,
            'message': 'User details updated successfully!!! '
        })
    except:
        pass
    resp = jsonify(message)
    return resp


@app.route('/employee/<int:id>', methods=['DELETE'])
def delete_emp(id):
    """
    This function will delete employee with given id

    """
    message = {
        'status': 404,
        'message': 'emp not found'
    }
    try:
        current_emp = Employee.query.get_or_404(id)
        db.session.delete(current_emp)
        db.session.commit()
        message.update({
            'status': 200,
            'message': 'user record delete successfully!!! '
        })
    except:
        pass
    resp = jsonify(message)
    return resp


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
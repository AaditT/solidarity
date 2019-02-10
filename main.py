from flask import *

app = Flask(__name__)


user_identity = None

class User():
    all_users = []
    def __init__(self, username, password):
        self.username = username
        self.password = password
    @staticmethod
    def login(username, password):
        global user_identity
        result = [user for user in User.all_users if (user.username == username and user.password == password)][0]
        user_identity = result

class RegisteredRefugee():
    all_registered = []
    def __init__(self, username, password, employer=None):
        self.username = username
        self.password = password
        self.employer = employer
        self.flagged = False
        RegisteredRefugee.all_registered.append(self)

class RegisteredEmployer():
    all_registered = []
    def __init__(self, name, credits=0):
        self.name = name
        self.credits = credits
        self.hired_refugees = []
        self.credit_record = []
        self.count = 0
        RegisteredEmployer.all_registered.append(self)
    def hire(self, refugee):
        refugee.employer = self
        self.hired_refugees.append(refugee)
        self.credits += 10
        self.credit_record.append(self.credits+0)
        self.count += 1
    def fire(self, refugee):
        refugee.employer = None
        self.hired_refugees.remove(refugee)
        if not refugee.flagged:
            self.credits -= 15
        self.credit_record.append(self.credits+0)
        self.count += 1
    @staticmethod
    def all_credit_data():
        return {employer.name:employer.credits for employer in RegisteredEmployer.all_registered}

# TRANSITIONS ----------------------------------------------

skynet = RegisteredEmployer('Skynet')
dunder_mifflin = RegisteredEmployer('DunderMifflin')
local_cafe = RegisteredEmployer('LocalCafe')
banana_co = RegisteredEmployer('BananaCo')
malik = RegisteredRefugee('malik', '123')
jacob = RegisteredRefugee('jacob', '123')
john = RegisteredRefugee('john', '123')
cindy = RegisteredRefugee('cindy', '123')
skynet.hire(malik)
dunder_mifflin.hire(cindy)
local_cafe.hire(RegisteredRefugee(None, None))
banana_co.hire(RegisteredRefugee(None, None))
skynet.fire(malik)
banana_co.hire(malik)
dunder_mifflin.hire(jacob)
skynet.hire(RegisteredRefugee(None, None))
dunder_mifflin.fire(cindy)
local_cafe.hire(RegisteredRefugee(None, None))
banana_co.hire(RegisteredRefugee(None, None))
banana_co.fire(malik)

# TRANSITIONS ----------------------------------------------

def gen_list(count):
    my_list = []
    for i in range(count):
        my_list.append(i)
    return my_list


@app.route('/graph/<employer_name>')
def graph(employer_name):
    employer = [employer for employer in RegisteredEmployer.all_registered if employer.name == employer_name][0]
    employer_credits = employer.credit_record
    x_vals=gen_list(int(employer.count))
    return render_template('graph.html', x_vals=x_vals,employer_credits=employer_credits,employer=employer_name)

@app.route('/user/<username>')
def user_page(username):
    user = [refugee for refugee in RegisteredRefugee.all_registered if refugee.username == username][0]
    return render_template('refugee_home.html', user=user)

@app.route('/employer/<employer_name>')
def employer_page(employer_name):
    employer = [employer for employer in RegisteredEmployer.all_registered if employer.name == employer_name][0]
    return render_template('employer_home.html', employer=employer)

@app.route('/', methods=['GET','POST'])
def home():
    all_employers = RegisteredEmployer.all_registered
    return render_template('index.html',all_employers=all_employers)
@app.route('/hired', methods=['GET','POST'])
def hire():
    if request.method == 'POST':
        username = str(request.form['refugee'])
        user = [refugee for refugee in RegisteredRefugee.all_registered if refugee.username == username][0]
        employer_name = str(request.form['employer'])
        employer = [employer for employer in RegisteredEmployer.all_registered if employer.name == employer_name][0]
        employer.hire(user)
    all_employers = RegisteredEmployer.all_registered
    return render_template('index.html', all_employers=all_employers)

@app.route('/fired', methods=['GET','POST'])
def fire():
    if request.method == 'POST':
        username = str(request.form['refugee'])
        user = [refugee for refugee in RegisteredRefugee.all_registered if refugee.username == username][0]
        employer_name = str(request.form['employer'])
        employer = [employer for employer in RegisteredEmployer.all_registered if employer.name == employer_name][0]
        employer.fire(user)
    all_employers = RegisteredEmployer.all_registered
    return render_template('index.html', all_employers=all_employers)

@app.route('/flagged', methods=['GET','POST'])
def flag():
    if request.method == 'POST':
        employer_name = str(request.form['employer'])
        employer = [employer for employer in RegisteredEmployer.all_registered if employer.name == employer_name][0]
        refugee_name = str(request.form['refugee'])
        refugee = [refugee for refugee in RegisteredRefugee.all_registered if refugee.username == refugee_name][0]
        refugee.flagged = True
    all_employers = RegisteredEmployer.all_registered
    return render_template('index.html', all_employers=all_employers)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        refugee = [refugee for refugee in RegisteredRefugee.all_registered if (refugee.username == username and refugee.password == password)][0]
        return render_template('refugee_home.html', user=refugee)
    return render_template('index.html', all_employers=all_employers)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)

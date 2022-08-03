from flask import (Flask, render_template, request, redirect, session)
import mysql.connector

#Todo need to mask the username and password
def mysql_connection():
    temp_cox = mysql.connector.connect(host='localhost', port=3306, database='lms', user='shubho', password='shubho')
    temp_curr = temp_cox.cursor()
    return temp_cox,temp_curr


def select_query(query):
    try:
        con,cursor = mysql_connection()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        con.close()
        return result
    except mysql.connector.Error as err:
        print(err)

user = select_query("SELECT `EMP_ID` FROM `employee_details`;")
user =[i[0] for i in user]


def employee_leave_creation(emp_id):
    result = select_query('SELECT * FROM `lu_leave`;')
    try:
        conx,curr =mysql_connection()
        for i in result:
            sql = '''INSERT INTO `emp_leave_balance` (`EMP_ID`,`LAEAVE_TYPE_ID`,`LAEAVE_COUNT`)
                  VALUES (%s,%s,%s)'''
            value =(emp_id,i[0],i[1])
            # print(sql,value)
            curr.execute(sql,value)
            conx.commit()
        curr.close()
        conx.close()
    except mysql.connector.Error as err:
        print(err)





app = Flask(__name__)
#Todo need to mask the secret_key
app.secret_key ='Shubho'


@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route('/add_employee', methods=['POST', 'GET'])
def add_employee():
    if (request.method == 'POST'):
        firstName = str(request.form.get('firstName'))
        middleName = str(request.form.get('middleName'))
        lastName = str(request.form.get('lastName'))
        isMan = request.form.get('isMan')
        if isMan == "":
            isMan = 0
        manID = request.form.get('manID')
        if manID == "":
            manID = 1
        contactDetails = request.form.get('contactDetails')
        password = str(request.form.get('password'))
        conn,curr = mysql_connection()
        try:
            sql = '''INSERT INTO `employee_details`
            (`EMP_FNAME`,`EMP_MNAME`,`EMP_LNAME`,`IS_MAN`,`MAN_ID`,`EMP_CONTACT_NO`,`EMP_PASSWORD`)
             VALUES (%s,%s,%s,%s,%s,%s,%s)'''
            value = (firstName,middleName,lastName,isMan,manID,contactDetails,password)
            # print(sql,value)
            curr.execute(sql,value)
            conn.commit()
            curr.close()
            query_output = select_query("SELECT `EMP_ID` FROM `employee_details` ORDER BY `EMP_ID` DESC LIMIT 1;")
            emp_id = [i[0] for i in query_output][0]
            employee_leave_creation(emp_id)

            # print(curr.rowcount, "details inserted")
            return redirect('/')
        except mysql.connector.Error as err:
            print(err)
            conn.rollback()
            conn.close()
            return '''<h1>Due faluty data entry. User hasnt been created please try again.</h1> <ul>
         <li><a href="http://localhost:8081/login">Login as Manager</a>   </li>
    <li> <a href="http://localhost:8081/login">Login as Employee</a>   </li>
    <li> <a href="http://localhost:8081/add_employee">Add Employee</a> </li>
    <li>  <a href="http://localhost:8081/">Home</a>  </li></ul>'''
        finally:
            conn.close()


    return render_template("add_employee.html")


@app.route('/login_man', methods=['POST', 'GET'])
def login_man():
    if (request.method == 'POST'):
        myresult = select_query('SELECT `EMP_ID`,`EMP_PASSWORD`,`IS_MAN`,`MAN_ID` FROM `employee_details` where IS_MAN="1";')
        username = request.form.get('username')
        password = request.form.get('password')
        for temp_emp_id,temp_pass,temp_is_man,temp_man_id in myresult:
            if int(temp_emp_id)==int(username) and temp_pass==password:
                session['user'] = int(username)
                session['temp_is_man'] = temp_is_man
                session['temp_man_id'] = int(temp_man_id)
                return redirect('/dashboard')
        return "<h1>Wrong username or password. </h1>"

    return render_template("login_man.html")


@app.route('/login_emp', methods=['POST', 'GET'])
def login_emp():
    if (request.method == 'POST'):
        myresult = select_query('SELECT `EMP_ID`,`EMP_PASSWORD`,`IS_MAN`,`MAN_ID` FROM `employee_details`;')
        username = request.form.get('username')
        password = request.form.get('password')
        for temp_emp_id,temp_pass,temp_is_man,temp_man_id in myresult:
            if int(temp_emp_id)==int(username) and temp_pass==password:
                session['user'] = int(username)
                session['temp_is_man'] = temp_is_man
                session['temp_man_id'] = int(temp_man_id)
                return redirect('/dashboard')
        return "<h1>Wrong username or password</h1>"

    return render_template("login_emp.html")


@app.route('/dashboard')
def dashboard():
    if ('user' in session and session['user'] in user):
        # print(session['temp_is_man'])
        if 'temp_is_man' in session and session['temp_is_man'] == 0:
            emp_id = session['user']
            # print(emp_id)
            try:

                conn, curr = mysql_connection()
                emp_id=4
                sql= ('SELECT * FROM `emp_leave_balance` where emp_id = %s;')
                val =(emp_id,)
                curr.execute(sql, val)
                query_result = curr.fetchall()
                curr.close()
                conn.close()
                leave_type = []
                # leave_count = []
                for i in query_result:
                    leave_type.append((i[1],i[-1]))
                    # leave_count.append()
                return render_template('employee.html',leave_type= tuple(leave_type))
                # '<h1>Welcome to the Employee dashboard</h1>'
            except mysql.connector.Error as err:
                print(err)
                return '<h1>Unable to the retreive Employee data</h1>'

        else:
            return '<h1>Welcome to the Manager dashboard</h1>'


    return '<h1>You are not logged in.</h1>'


@app.route('/apply',methods=['POST', 'GET'])
def apply():
    if (request.method == 'POST'):
        start_date = request.form.get('startDate')
        end_date = request.form.get('endDate')
        leave_type = request.form.get('leaveType')
        emp_id = session['user']
        sql = '''INSERT INTO `leave_status` (`EMP_ID`,`LAEAVE_TYPE_ID`,`START_DATE`,`END_DATE`)
                          VALUES (%s,%s,%s,%s,%s)'''
        value = (emp_id, leave_type,start_date,end_date)

        sql_leave_balance = 'UPDATE `emp_leave_balance` SET `LAEAVE_COUNT`= `LAEAVE_COUNT` - 1 WHERE `LAEAVE_TYPE_ID` = %s'
        val_leave_balance = leave_type.upper()
        try:
            conn, curr = mysql_connection()
            try:
                curr.execute(sql, value)
                curr.execute(sql_leave_balance, val_leave_balance)
                conn.commit()
                curr.close()
            except mysql.connector.Error as err:
                print(err)

        except mysql.connector.Error as err:
            print(err)


    return render_template('apply.html')


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/login')


if __name__ == '__main__':
    app.run(port=8081 ,debug=True)
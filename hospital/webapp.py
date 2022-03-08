import sys
from os import name
from flask import Flask, render_template
from flask import request, redirect
from flask.helpers import url_for
from hospital.db_connector import connect_to_database, execute_query

#create the web application
webapp = Flask(__name__)

@webapp.route('/')
def main():
    return render_template('index.html')


@webapp.route('/index')
def index():
    return render_template('index.html')


@webapp.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    # idList = id.split()
    # # idList = [int(i) for i in id.split()]
    # id = int(idList[0])

    db_connection = connect_to_database()
    table = request.args.get('table')

    if request.method == 'POST' and "updateButton" in request.form: # verify
        doctorRes = ""
        nurseRes = ""
        patientRes = ""
        prescriptionRes = ""
        npRes = ""

        if table == 'doctors':
            query = "SELECT doctorID, doctorName, doctorSpecialty, doctorPhone from Doctors WHERE doctorID=%d;" % (id)
            doctorRes = execute_query(db_connection, query).fetchall()[0]

        elif table == 'nurses':
            query = "SELECT nurseID, nurseName, nurseFloor, nursePhone from Nurses WHERE nurseID=%d;" % (id)
            nurseRes = execute_query(db_connection, query).fetchall()[0]

        elif table == 'patients':
            patQuery = "SELECT Patients.patientID, Patients.patientName, Patients.patientInsuranceNo, Patients.patientRoom, Patients.patientPhone, Doctors.doctorID, Doctors.doctorName, Prescriptions.prescriptionID, Prescriptions.prescriptionDetails FROM Patients LEFT JOIN Prescriptions ON Patients.prescriptionID = Prescriptions.prescriptionID LEFT JOIN Doctors ON Patients.doctorID = Doctors.doctorID WHERE Patients.patientID=%d;" % (id)
            patientRes = execute_query(db_connection, patQuery).fetchall()[0]

            docQuery = "SELECT doctorID, doctorName from Doctors;"
            doctorRes = execute_query(db_connection, docQuery).fetchall()

        elif table == 'prescriptions':
            preQuery = "SELECT Prescriptions.prescriptionID, Prescriptions.prescriptionDetails, Prescriptions.prescriptionDate, Patients.patientID, Patients.patientName, Doctors.doctorID, Doctors.doctorName FROM Prescriptions LEFT JOIN Patients ON Prescriptions.patientID = Patients.patientID LEFT JOIN Doctors ON Prescriptions.doctorID = Doctors.doctorID WHERE Prescriptions.prescriptionID=%d;" % (id)
            prescriptionRes = execute_query(db_connection, preQuery).fetchall()[0]

            patQuery = "SELECT patientID, patientName from Patients;"
            patientRes = execute_query(db_connection, patQuery).fetchall()

            docQuery = "SELECT doctorID, doctorName from Doctors;"
            doctorRes = execute_query(db_connection, docQuery).fetchall()

        # elif table == 'nursesPatients':
        #     print("NNNNNNNNNNN\nNURSE ID, PATIENT ID", idList[0], idList[1])
        #     npQuery = "SELECT nursesPatients2.nurseID, Nurses.nurseName, nursesPatients2.patientID, Patients.patientName FROM nursesPatients2 LEFT JOIN Nurses ON nursesPatients2.nurseID = Nurses.nurseID LEFT JOIN Patients ON nursesPatients2.patientID = Patients.patientID WHERE nursesPatients2.nurseID=%s AND nursesPatients2.patientID=%s;" % (idList[0], idList[1])
        #     npRes = execute_query(db_connection, npQuery).fetchall()[0]

        #     print('\n\n npres!!! ', npRes)
        #     patQuery = "SELECT patientID, patientName from Patients;"
        #     patientRes = execute_query(db_connection, patQuery).fetchall()

        #     nurseQuery = "SELECT nurseID, nurseName from Nurses;"
        #     nurseRes = execute_query(db_connection, nurseQuery).fetchall()

        else:
            return render_template('update_page.html')

        return render_template('update_page.html', table = table, doctors = doctorRes, nurses = nurseRes, patients = patientRes, prescriptions = prescriptionRes) #, nursesPatients = npRes)

    elif request.method == 'POST':
        if table == 'doctors':
            doctorName = request.form['doctorName']
            doctorPhone = request.form['doctorPhone']
            doctorSpecialty = request.form['doctorSpecialty']

            query = 'UPDATE Doctors SET doctorName=%s, doctorPhone=%s, doctorSpecialty=%s WHERE doctorID=%s;'
            data = (doctorName, doctorPhone, doctorSpecialty, str(id));
            execute_query(db_connection, query, data)
            return redirect(url_for('doctors'))

        if table == 'nurses':
            nurseName = request.form['nurseName']
            nursePhone = request.form['nursePhone']
            nurseFloor = request.form['nurseFloor']

            query = 'Update Nurses SET nurseName=%s, nursePhone=%s, nurseFloor=%s WHERE nurseID=%s'
            data = (nurseName, nursePhone, nurseFloor, str(id));
            execute_query(db_connection, query, data)
            return redirect(url_for('nurses'))

        if table == 'patients':
            patientName = request.form['patientName']
            patientPhone = request.form['patientPhone']
            patientRoom = request.form['patientRoom']
            patientInsuranceNo = request.form['patientInsuranceNo']
            doctorID = request.form['doctorID']
            # prescriptionID = request.form['prescriptionID']

            # query = 'INSERT INTO Patients (patientName, patientPhone, patientInsuranceNo, doctorID, prescriptionID) VALUES (%s, %s, %s, %s, %s)'
            # data = (patientName, patientPhone, patientInsuranceNo, doctorID, prescriptionID)
            query = 'UPDATE Patients SET patientName=%s, patientPhone=%s, patientRoom=%s, patientInsuranceNo=%s, doctorID=%s WHERE patientID=%s'
            data = (patientName, patientPhone, patientRoom, patientInsuranceNo, doctorID, str(id))
            execute_query(db_connection, query, data)
            return redirect(url_for('patients'))

        if table == 'prescriptions':
            prescriptionDetails = request.form['prescriptionDetails']
            prescriptionDate = request.form['prescriptionDate']
            doctorID = request.form['doctorID']
            patientID = request.form['patientID']

            query = 'UPDATE Prescriptions SET prescriptionDetails=%s, prescriptionDate=%s, doctorID=%s, patientID=%s WHERE prescriptionID=%s'
            data = (prescriptionDetails, prescriptionDate, doctorID, patientID, str(id));
            ret = execute_query(db_connection, query, data)

            if ret is not None:
                idQuery = "SELECT prescriptionID from Prescriptions WHERE patientID = %s;" % (patientID)
                idResult = execute_query(db_connection, idQuery).fetchall()

                updQuery = "UPDATE Patients SET prescriptionID = %s WHERE patientID = %s" % (idResult[0][0], patientID)
                execute_query(db_connection, updQuery)

            return redirect(url_for('prescriptions'))

        # if table == 'nursesPatients':
        #     print("NNNNNNNNNNN\nNURSE ID, PATIENT ID", idList[0], idList[1])
        #     nurseID = request.form['nurseID']
        #     patientID = request.form['patientID']

        #     npQuery = "SELECT nurseID, patientID FROM nursesPatients2 WHERE nurseID=%s AND patientID=%s;" % (nurseID, patientID)
        #     npRes = execute_query(db_connection, npQuery).fetchall()

        #     print('npres---', npRes)
        #     if npRes == (): # Only insert if it is not in there, just do nothing otherwise
        #         query = "UPDATE nursesPatients2 SET nurseID=%s, patientID=%s WHERE nurseID=%s AND patientID=%s;"
        #         data = (nurseID, patientID, nurseID, patientID);
        #         ret = execute_query(db_connection, query, data)

        #         #                 # NOTE: update doesn't work, just delete and re-insert
        #         # query = 'DELETE FROM nursesPatients2 WHERE nurseID=%s AND patientID=%s' % (nurseID, patientID)
        #         # ret = execute_query(db_connection, query)

        #         # query = 'INSERT INTO nursesPatients2 (nurseID, patientID) VALUES (%s, %s)'
        #         # data = (nurseID, patientID);
        #         # ret = execute_query(db_connection, query, data)

        #     return redirect(url_for('nursesPatients'))




@webapp.route('/doctors', methods=['POST','GET'])
def doctors():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = "SELECT doctorID, doctorName, doctorSpecialty, doctorPhone from Doctors"
        result = execute_query(db_connection, query).fetchall()
        return render_template('doctors.html', doctors = result)

    elif request.method == 'POST' and 'insertDoctor' in request.form: # TODO: and 'addItem' in request.form:
        doctorName = request.form['doctorName']
        doctorPhone = request.form['doctorPhone']
        doctorSpecialty = request.form['doctorSpecialty']

        query = 'INSERT INTO Doctors (doctorName, doctorPhone, doctorSpecialty) VALUES (%s, %s, %s)'
        data = (doctorName, doctorPhone, doctorSpecialty);
        execute_query(db_connection, query, data)
        return redirect(url_for('doctors'))

    elif request.method == 'POST' and 'deleteDoctor' in request.form:
        doctorID = request.form['doctorID']

        query = 'DELETE FROM Doctors WHERE doctorID = %s' % (doctorID)
        result = execute_query(db_connection, query).fetchall()
        return redirect(url_for('doctors'))


@webapp.route('/nurses', methods=['POST','GET'])
def nurses():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = "SELECT nurseID, nurseName, nurseFloor, nursePhone from Nurses;"
        result = execute_query(db_connection, query).fetchall()

        finalResult = ()
        for nurse in result:
            nid = nurse[0]
            patQuery = "SELECT patientID FROM nursesPatients2 WHERE nurseID = %s;" % (nid)
            patRes = execute_query(db_connection, patQuery).fetchall()
            if patRes == ():
                finalResult = finalResult + (nurse,)
                continue

            else:
                # Had some issues with patres being formatted wrong, these lines fix it:
                patRes = [item for subl in patRes for item in subl]
                patRes = str(patRes).replace('[', '(').replace(']', ')') # format in a nice format for the query

                patNameQuery = "SELECT patientName FROM Patients WHERE patientID IN " + str(patRes)
                patNameRes = execute_query(db_connection, patNameQuery).fetchall()

                # Had some issues with patres being formatted wrong, these lines fix it:
                patNameRes = [item for subl in patNameRes for item in subl]
                patNameRes = tuple(patNameRes)

                finalResult = finalResult + (nurse + (patNameRes,),)   # finally put all this work back into original thing

        return render_template('nurses.html', nurses = finalResult)

    elif request.method == 'POST' and 'insertNurse' in request.form: # TODO: and 'addItem' in request.form:
        nurseName = request.form['nurseName']
        nursePhone = request.form['nursePhone']
        nurseFloor = request.form['nurseFloor']

        query = 'INSERT INTO Nurses (nurseName, nursePhone, nurseFloor) VALUES (%s, %s, %s)'
        data = (nurseName, nursePhone, nurseFloor);
        execute_query(db_connection, query, data)
        return redirect(url_for('nurses'))

    elif request.method == 'POST' and 'deleteNurse' in request.form:
        nurseID = request.form['nurseID']

        query = 'DELETE FROM Nurses WHERE nurseID = %s' % (nurseID)
        result = execute_query(db_connection, query).fetchall()
        return redirect(url_for('nurses'))


@webapp.route('/patients', methods=['POST','GET'])
def patients():
    db_connection = connect_to_database()
    if request.method == 'GET':
        patQuery = "SELECT Patients.patientID, Patients.patientName, Patients.patientInsuranceNo, Patients.patientRoom, Patients.patientPhone, Doctors.doctorID, Doctors.doctorName, Prescriptions.prescriptionID, Prescriptions.prescriptionDetails FROM Patients LEFT JOIN Prescriptions ON Patients.prescriptionID = Prescriptions.prescriptionID LEFT JOIN Doctors ON Patients.doctorID = Doctors.doctorID;"
        patResult = execute_query(db_connection, patQuery).fetchall()

        finalPatResult = ()
        for patient in patResult:
            pid = patient[0]
            nurQuery = "SELECT nurseID FROM nursesPatients2 WHERE patientID = %s;" % (pid)
            nurRes = execute_query(db_connection, nurQuery).fetchall()
            if nurRes == ():
                finalPatResult = finalPatResult + (patient,)
                continue

            else:
                # Had some issues with patres being formatted wrong, these lines fix it:
                nurRes = [item for subl in nurRes for item in subl]
                nurRes = str(nurRes).replace('[', '(').replace(']', ')') # format in a nice format for the query

                nurNameQuery = "SELECT nurseName FROM Nurses WHERE nurseID IN " + str(nurRes)
                nurNameRes = execute_query(db_connection, nurNameQuery).fetchall()

                # Had some issues with patres being formatted wrong, these lines fix it:
                nurNameRes = [item for subl in nurNameRes for item in subl]
                nurNameRes = tuple(nurNameRes)

                finalPatResult = finalPatResult + (patient + (nurNameRes,),)   # finally put all this work back into original thing


        docQuery = "SELECT doctorID, doctorName from Doctors;"
        docResult = execute_query(db_connection, docQuery).fetchall()

        # NOTE: It doesn't really make sense to add prescription here, it's made on a per-patient basis.
        #        just assign on prescription side

        return render_template('patients.html', patients = finalPatResult, doctors = docResult)

    elif request.method == 'POST' and 'insertPatient' in request.form: # TODO: and 'addItem' in request.form:
        patientName = request.form['patientName']
        patientPhone = request.form['patientPhone']
        patientRoom = request.form['patientRoom']
        patientInsuranceNo = request.form['patientInsuranceNo']
        doctorID = request.form['doctorID']
        # prescriptionID = request.form['prescriptionID']

        # query = 'INSERT INTO Patients (patientName, patientPhone, patientInsuranceNo, doctorID, prescriptionID) VALUES (%s, %s, %s, %s, %s)'
        # data = (patientName, patientPhone, patientInsuranceNo, doctorID, prescriptionID)
        query = 'INSERT INTO Patients (patientName, patientPhone, patientRoom, patientInsuranceNo, doctorID) VALUES (%s, %s, %s, %s, %s)'
        data = (patientName, patientPhone, patientRoom, patientInsuranceNo, doctorID)
        execute_query(db_connection, query, data)
        return redirect(url_for('patients'))

    elif request.method == 'POST' and 'deletePatient' in request.form:
        patientID = request.form['patientID']

        query = 'DELETE FROM Patients WHERE patientID = %s' % (patientID)
        result = execute_query(db_connection, query).fetchall()
        return redirect(url_for('patients'))


@webapp.route('/prescriptions', methods=['POST','GET'])
def prescriptions():
    db_connection = connect_to_database()
    if request.method == 'GET':
        preQuery = "SELECT Prescriptions.prescriptionID, Prescriptions.prescriptionDetails, Prescriptions.prescriptionDate, Patients.patientID, Patients.patientName, Doctors.doctorID, Doctors.doctorName FROM Prescriptions LEFT JOIN Patients ON Prescriptions.patientID = Patients.patientID LEFT JOIN Doctors ON Prescriptions.doctorID = Doctors.doctorID;"
        preResult = execute_query(db_connection, preQuery).fetchall()
        patQuery = "SELECT patientID, patientName from Patients WHERE prescriptionID IS NULL;"
        patResult = execute_query(db_connection, patQuery).fetchall()

        docQuery = "SELECT doctorID, doctorName from Doctors;"
        docResult = execute_query(db_connection, docQuery).fetchall()
        return render_template('prescriptions.html', prescriptions = preResult, patients = patResult, doctors = docResult)

    elif request.method == 'POST' and 'insertPrescription' in request.form:
        prescriptionDetails = request.form['prescriptionDetails']
        prescriptionDate = request.form['prescriptionDate']
        doctorID = request.form['doctorID']
        patientID = request.form['patientID']

        query = 'INSERT INTO Prescriptions (prescriptionDetails, prescriptionDate, doctorID, patientID) VALUES (%s, %s, %s, %s)'
        data = (prescriptionDetails, prescriptionDate, doctorID, patientID);
        ret = execute_query(db_connection, query, data)

        if ret is not None:
            idQuery = "SELECT prescriptionID from Prescriptions WHERE patientID = %s;" % (patientID)
            idResult = execute_query(db_connection, idQuery).fetchall()

            updQuery = "UPDATE Patients SET prescriptionID = %s WHERE patientID = %s" % (idResult[0][0], patientID)
            execute_query(db_connection, updQuery)

        return redirect(url_for('prescriptions'))

    elif request.method == 'POST' and 'deletePrescription' in request.form:
        prescriptionID = request.form['prescriptionID']
        patientID = request.form['patientID']

        updQuery = "UPDATE Patients SET prescriptionID = %s WHERE patientID = %s" % ('NULL', patientID)
        execute_query(db_connection, updQuery)

        query = 'DELETE FROM Prescriptions WHERE prescriptionID = %s' % (prescriptionID)
        result = execute_query(db_connection, query).fetchall()
        return redirect(url_for('prescriptions'))



@webapp.route('/nursesPatients', methods=['POST','GET'])
def nursesPatients():
    db_connection = connect_to_database()
    if request.method == 'GET':
        npQuery = "SELECT nursesPatients2.nurseID, Nurses.nurseName, nursesPatients2.patientID, Patients.patientName FROM nursesPatients2 LEFT JOIN Nurses ON nursesPatients2.nurseID = Nurses.nurseID LEFT JOIN Patients ON nursesPatients2.patientID = Patients.patientID;"
        npResult = execute_query(db_connection, npQuery).fetchall()


        patQuery = "SELECT patientID, patientName from Patients;"
        patResult = execute_query(db_connection, patQuery).fetchall()

        nurseQuery = "SELECT nurseID, nurseName from Nurses;"
        nurseResult = execute_query(db_connection, nurseQuery).fetchall()
        return render_template('nursesPatients.html', nursesPatients = npResult, patients = patResult, nurses = nurseResult)

    elif request.method == 'POST' and 'insertNursesPatients' in request.form:
        nurseID = request.form['nurseID']
        patientID = request.form['patientID']

        npQuery = "SELECT nurseID, patientID FROM nursesPatients2 WHERE nurseID=%s AND patientID=%s;" % (nurseID, patientID)
        npRes = execute_query(db_connection, npQuery).fetchall()

        if npRes == (): # Only insert if it is not in there, just do nothing otherwise
            query = 'INSERT INTO nursesPatients2 (nurseID, patientID) VALUES (%s, %s)'
            data = (nurseID, patientID);
            ret = execute_query(db_connection, query, data)

        return redirect(url_for('nursesPatients'))


    elif request.method == 'POST' and 'deleteNursesPatients' in request.form:
        nurseID = request.form['nurseID']
        patientID = request.form['patientID']

        query = 'DELETE FROM nursesPatients2 WHERE nurseID=%s AND patientID=%s' % (nurseID, patientID)
        result = execute_query(db_connection, query).fetchall()
        return redirect(url_for('nursesPatients'))


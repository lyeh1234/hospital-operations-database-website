
-- Doctor:
SELECT doctorID, doctorName, doctorSpecialty, doctorPhone from Doctors WHERE doctorID=%d;
SELECT doctorID, doctorName from Doctors;
SELECT doctorID, doctorName, doctorSpecialty, doctorPhone from Doctors

INSERT INTO Doctors (doctorName, doctorPhone, doctorSpecialty) VALUES (%s, %s, %s)

UPDATE Doctors SET doctorName=%s, doctorPhone=%s, doctorSpecialty=%s WHERE doctorID=%s;

DELETE FROM Doctors WHERE doctorID = %s



-- Nurse:
SELECT nurseID, nurseName, nurseFloor, nursePhone from Nurses WHERE nurseID=%d;
SELECT nurseID, nurseName from Nurses;
SELECT nurseID, nurseName, nurseFloor, nursePhone from Nurses;
SELECT nurseID FROM nursesPatients2 WHERE patientID = %s;
SELECT nurseName FROM Nurses WHERE nurseID IN %s

INSERT INTO Nurses (nurseName, nursePhone, nurseFloor) VALUES (%s, %s, %s)

Update Nurses SET nurseName=%s, nursePhone=%s, nurseFloor=%s WHERE nurseID=%s

DELETE FROM Nurses WHERE nurseID = %s



-- Patients:
SELECT Patients.patientID, Patients.patientName, Patients.patientInsuranceNo, Patients.patientRoom, Patients.patientPhone, Doctors.doctorID, Doctors.doctorName, Prescriptions.prescriptionID, Prescriptions.prescriptionDetails FROM Patients LEFT JOIN Prescriptions ON Patients.prescriptionID = Prescriptions.prescriptionID LEFT JOIN Doctors ON Patients.doctorID = Doctors.doctorID WHERE Patients.patientID=%d;
SELECT patientID, patientName from Patients;
SELECT patientID FROM nursesPatients2 WHERE nurseID = %s;
SELECT patientName FROM Patients WHERE patientID IN %s
SELECT Patients.patientID, Patients.patientName, Patients.patientInsuranceNo, Patients.patientRoom, Patients.patientPhone, Doctors.doctorID, Doctors.doctorName, Prescriptions.prescriptionID, Prescriptions.prescriptionDetails FROM Patients LEFT JOIN Prescriptions ON Patients.prescriptionID = Prescriptions.prescriptionID LEFT JOIN Doctors ON Patients.doctorID = Doctors.doctorID;
SELECT patientID, patientName from Patients WHERE prescriptionID IS NULL;

INSERT INTO Patients (patientName, patientPhone, patientRoom, patientInsuranceNo, doctorID) VALUES (%s, %s, %s, %s, %s)

UPDATE Patients SET patientName=%s, patientPhone=%s, patientRoom=%s, patientInsuranceNo=%s, doctorID=%s WHERE patientID=%s
UPDATE Patients SET prescriptionID = %s WHERE patientID = %s

DELETE FROM Patients WHERE patientID = %s



-- Prescriptions:
SELECT Prescriptions.prescriptionID, Prescriptions.prescriptionDetails, Prescriptions.prescriptionDate, Patients.patientID, Patients.patientName, Doctors.doctorID, Doctors.doctorName FROM Prescriptions LEFT JOIN Patients ON Prescriptions.patientID = Patients.patientID LEFT JOIN Doctors ON Prescriptions.doctorID = Doctors.doctorID;
SELECT Prescriptions.prescriptionID, Prescriptions.prescriptionDetails, Prescriptions.prescriptionDate, Patients.patientID, Patients.patientName, Doctors.doctorID, Doctors.doctorName FROM Prescriptions LEFT JOIN Patients ON Prescriptions.patientID = Patients.patientID LEFT JOIN Doctors ON Prescriptions.doctorID = Doctors.doctorID WHERE Prescriptions.prescriptionID=%d;
SELECT prescriptionID from Prescriptions WHERE patientID = %s;

INSERT INTO Prescriptions (prescriptionDetails, prescriptionDate, doctorID, patientID) VALUES (%s, %s, %s, %s)

UPDATE Patients SET prescriptionID = %s WHERE patientID = %s
UPDATE Prescriptions SET prescriptionDetails=%s, prescriptionDate=%s, doctorID=%s, patientID=%s WHERE prescriptionID=%s

DELETE FROM Prescriptions WHERE prescriptionID = %s


-- nursesPatients:
SELECT nursesPatients2.nurseID, Nurses.nurseName, nursesPatients2.patientID, Patients.patientName FROM nursesPatients2 LEFT JOIN Nurses ON nursesPatients2.nurseID = Nurses.nurseID LEFT JOIN Patients ON nursesPatients2.patientID = Patients.patientID;
SELECT nurseID, patientID FROM nursesPatients2 WHERE nurseID=%s AND patientID=%s;

INSERT INTO nursesPatients2 (nurseID, patientID) VALUES (%s, %s)

DELETE FROM nursesPatients2 WHERE nurseID=%s AND patientID=%s

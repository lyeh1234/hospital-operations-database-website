-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Dec 08, 2020 at 05:29 AM
-- Server version: 10.4.15-MariaDB-log
-- PHP Version: 7.4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cs340_hartmank`
--

-- --------------------------------------------------------

--
-- Table structure for table `Doctors`
--

CREATE TABLE `Doctors` (
  `doctorID` int(11) NOT NULL,
  `doctorSpecialty` varchar(255) NOT NULL,
  `doctorName` varchar(255) NOT NULL,
  `doctorPhone` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Doctors`
--

INSERT INTO `Doctors` (`doctorID`, `doctorSpecialty`, `doctorName`, `doctorPhone`) VALUES
(5, 'Pediatrician', 'Johnny Eyeri update test', 2147345345),
(7, 'Dermatologist', 'Herb Skinson', 214748387),
(8, 'Surgeon', 'Bart Simpson', 2147483647),
(9, 'Pediatrician', 'Julie Pedaroy', 2),
(24, 'The Science Guy', 'Bill Nye', 123456789);

-- --------------------------------------------------------

--
-- Table structure for table `Nurses`
--

CREATE TABLE `Nurses` (
  `nurseID` int(11) NOT NULL,
  `nurseName` varchar(255) NOT NULL,
  `nursePhone` int(11) NOT NULL,
  `nurseFloor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Nurses`
--

INSERT INTO `Nurses` (`nurseID`, `nurseName`, `nursePhone`, `nurseFloor`) VALUES
(8, 'Laura Holmes', 2147483647, 2),
(9, 'Diana Fickes', 2147483647, 1),
(11, 'Leela', 2147483647, 2),
(16, 'test nurse 2', 2147483647, 8),
(18, 'Jackie Peyton', 1234567890, 5);

-- --------------------------------------------------------

--
-- Table structure for table `nursesPatients2`
--

CREATE TABLE `nursesPatients2` (
  `npID` int(11) NOT NULL,
  `nurseID` int(11) NOT NULL,
  `patientID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `nursesPatients2`
--

INSERT INTO `nursesPatients2` (`npID`, `nurseID`, `patientID`) VALUES
(0, 8, 6),
(0, 8, 7),
(3, 11, 9),
(4, 11, 10),
(0, 18, 8);

-- --------------------------------------------------------

--
-- Table structure for table `Patients`
--

CREATE TABLE `Patients` (
  `patientID` int(11) NOT NULL,
  `patientName` varchar(255) NOT NULL,
  `patientPhone` int(11) NOT NULL,
  `patientRoom` int(11) DEFAULT NULL,
  `patientInsuranceNo` int(11) NOT NULL,
  `doctorID` int(11) NOT NULL,
  `prescriptionID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Patients`
--

INSERT INTO `Patients` (`patientID`, `patientName`, `patientPhone`, `patientRoom`, `patientInsuranceNo`, `doctorID`, `prescriptionID`) VALUES
(6, 'Tiffany Jackson', 2147483647, 215, 998845, 5, 8),
(7, 'Jackie Anderson', 2147483647, 352, 985622, 8, NULL),
(8, 'Nate Snyder', 2147483647, 114, 567461, 7, 6),
(9, 'Jake Paul', 2147483647, 404, 651887, 9, NULL),
(10, 'Andy Wang', 2147483647, 119, 984615, 5, NULL),
(11, 'Linda Reynolds', 2147483647, 422, 847918, 8, 7),
(12, 'Tyler Crayon', 1112204687, 257, 668811, 7, NULL),
(13, 'Megan Bates', 1140901933, 377, 508749, 9, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `Prescriptions`
--

CREATE TABLE `Prescriptions` (
  `prescriptionID` int(11) NOT NULL,
  `prescriptionDetails` text NOT NULL,
  `prescriptionDate` date NOT NULL,
  `doctorID` int(11) NOT NULL,
  `patientID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Prescriptions`
--

INSERT INTO `Prescriptions` (`prescriptionID`, `prescriptionDetails`, `prescriptionDate`, `doctorID`, `patientID`) VALUES
(6, 'See recommended Physical Therapist', '2020-11-10', 7, 8),
(7, 'Tylenol and Pedialyte', '2020-12-24', 5, 11),
(8, 'Every third Tuesday, be sure to eat half of apple and chug 12oz root beer', '0000-00-00', 6, 6);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Doctors`
--
ALTER TABLE `Doctors`
  ADD PRIMARY KEY (`doctorID`);

--
-- Indexes for table `Nurses`
--
ALTER TABLE `Nurses`
  ADD PRIMARY KEY (`nurseID`);

--
-- Indexes for table `nursesPatients2`
--
ALTER TABLE `nursesPatients2`
  ADD PRIMARY KEY (`nurseID`,`patientID`),
  ADD KEY `fk_nurseID` (`nurseID`) USING BTREE,
  ADD KEY `fk_patID` (`patientID`) USING BTREE;

--
-- Indexes for table `Patients`
--
ALTER TABLE `Patients`
  ADD PRIMARY KEY (`patientID`);

--
-- Indexes for table `Prescriptions`
--
ALTER TABLE `Prescriptions`
  ADD PRIMARY KEY (`prescriptionID`),
  ADD UNIQUE KEY `patientID` (`patientID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Doctors`
--
ALTER TABLE `Doctors`
  MODIFY `doctorID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `Nurses`
--
ALTER TABLE `Nurses`
  MODIFY `nurseID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `Patients`
--
ALTER TABLE `Patients`
  MODIFY `patientID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `Prescriptions`
--
ALTER TABLE `Prescriptions`
  MODIFY `prescriptionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `nursesPatients2`
--
ALTER TABLE `nursesPatients2`
  ADD CONSTRAINT `fk_nurseID` FOREIGN KEY (`nurseID`) REFERENCES `Nurses` (`nurseID`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_patID` FOREIGN KEY (`patientID`) REFERENCES `Patients` (`patientID`) ON DELETE CASCADE;

--
-- Constraints for table `Prescriptions`
--
ALTER TABLE `Prescriptions`
  ADD CONSTRAINT `fk_patient_id` FOREIGN KEY (`patientID`) REFERENCES `Patients` (`patientID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

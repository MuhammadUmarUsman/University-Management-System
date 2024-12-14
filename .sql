create table Department(
	DID    int    primary key,
	Dname  varchar(30),
	Budget int
)
INSERT INTO Department VALUES
(1, 'Computer Science', 100000),
(2, 'Physics', 75000),
(3, 'Biology', 90000),
(4, 'Mathematics', 80000),
(5, 'Chemistry', 85000);



create table Student(
	SID    int    primary key,
	Sname  varchar(30),
	Addrss varchar(50),
	Age    int,
	DID    int    references Department(DID)
)
INSERT INTO Student VALUES
(101, 'Ali Khan', '123 Main Street, Karachi', 21, 1),
(102, 'Sana Ahmed', '456 Park Avenue, Lahore', 20, 2),
(103, 'Ahmed Malik', '789 Beach Road, Islamabad', 22, 1),
(104, 'Ayesha Khan', '567 Green Town, Lahore', 21, 2),
(105, 'Usman Riaz', '987 Blue Area, Islamabad', 23, 3),
(106, 'Fariha Siddiqui', '234 Cantt Road, Rawalpindi', 20, 1),
(107, 'Zubair Khan', '678 Model Colony, Karachi', 14, 4),
(108, 'Hina Akhtar', '345 Gulshan-e-Iqbal, Karachi', 22, 3),
(109, 'Imran Ali', '876 DHA, Lahore', 23, 4),
(110, 'Nida Hassan', '543 Satellite Town, Rawalpindi', 21, 5);

create table Faculty(
	FID    int    primary key,
	Fname  varchar(30),
	Salary int,
	Age    int,
	DID    int    references Department(DID)
)
INSERT INTO Faculty VALUES
(201, 'Dr. Nadeem Qureshi', 80000, 45, 1),
(202, 'Prof. Farida Hussain', 90000, 50, 2),
(203, 'Dr. Asad Malik', 85000, 42, 1),
(204, 'Prof. Aisha Rahman', 95000, 55, 2),
(205, 'Dr. Kamran Ahmed', 82000, 40, 3),
(206, 'Prof. Sarah Ali', 87000, 48, 1),
(207, 'Dr. Yasir Khan', 83000, 41, 4),
(208, 'Prof. Nadia Amin', 92000, 53, 3),
(209, 'Dr. Rashid Abbas', 84000, 43, 4),
(210, 'Prof. Sadia Iqbal', 91000, 52, 5);

create table Class(
	CID   int   primary key,
	CTime time,
	FID   int   references Faculty(FID)
)
INSERT INTO Class VALUES
(301, '09:00:00', 201),
(302, '11:00:00', 202),
(303, '10:30:00', 202),
(304, '12:30:00', 204),
(305, '13:00:00', 205),
(306, '14:00:00', 206),
(307, '15:30:00', 207),
(308, '16:30:00', 208),
(309, '14:30:00', 209),
(310, '17:00:00', 210);


create table Enrolled(
	SID    int    references Student(SID),
	CID    int    references Class(CID)
)
INSERT INTO Enrolled VALUES
(101, 301),
(101, 302),
(101, 301),
(104, 302),
(105, 303),
(106, 301),
(107, 304),
(108, 303),
(109, 304),
(110, 305);

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
--Write a procedure that takes the department ID as input parameter and display the name of the faculty member of that department who is not taking any class.

CREATE PROCEDURE FacultyWithoutClasses @deptID INT
AS
BEGIN
    SELECT Fname
    FROM Faculty
    WHERE DID = @deptID AND FID NOT IN (
        SELECT DISTINCT FID
        FROM Class C
    );
END;

exec FacultyWithoutClasses @deptID = 1

DROP PROCEDURE FacultyWithoutClasses


----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--Write a procedure that takes student ID as input parameters and display the total number of enrolled classes and names of the faculty members teaching that student.

CREATE PROCEDURE GetStudentEnrollment @studentID INT
AS
BEGIN
    SELECT COUNT(E.CID) AS TotalEnrolledClasses,F.Fname
    FROM Enrolled as E
    INNER JOIN Class as C 
	ON E.CID = C.CID
    INNER JOIN Faculty as F 
	ON C.FID = F.FID
    WHERE E.SID = @studentID
    GROUP BY F.Fname;
END;

EXEC GetStudentEnrollment @studentID = 101;


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--write a procedure that takes the department ID as input parameter and display the information of that faculty member who is taking the highest number of classes in this department.

CREATE PROCEDURE GetFacultyWithMostClasses @deptID INT
AS
BEGIN
    SELECT TOP 1 F.FID, F.Fname, F.Salary
    FROM Faculty as F
    INNER JOIN Class as C 
	ON F.FID = C.FID
    WHERE F.DID = @deptID
    GROUP BY F.FID, F.Fname, F.Salary
    ORDER BY COUNT(C.CID) DESC;
END;

exec GetFacultyWithMostClasses @deptID = 1;



--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--Procedure to display the information of classes and faculty members teaching a student.

CREATE PROCEDURE GetStudentEnrollmentInfo @studentID INT
AS
    SELECT C.CID, C.CTime, F.Fname
    FROM Enrolled as E
    INNER JOIN Class as C 
	ON E.CID = C.CID
    INNER JOIN Faculty as F
	ON C.FID = F.FID
    WHERE E.SID = @studentID;
Go

exec GetStudentEnrollmentInfo 101

select * from Department
select * from Student
select * from Faculty
select * from Enrolled
select * from Class
----------------------------------------------------------------------------------------------------------------------------------------------------------

create trigger preventTableDrop
on database
for drop_table
as
print 'you are attempting to drop a table'
rollback transaction

drop table Department



Create Trigger StudentAge
On Student
For Insert
As
Declare @age int
Select @age = (select age from inserted)
If(@age>18)
begin
Print ' Student is successfully added'
end
Else
begin
Print ' student record can not be inserted'
end
Rollback Transaction
go

drop trigger StudentAge
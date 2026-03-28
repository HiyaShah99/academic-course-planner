-- create database ACP;
-- use ACP;

CREATE TABLE course (
     course_code VARCHAR(50) PRIMARY KEY,
     course_name VARCHAR(255),
     credits decimal NOT NULL,
     faculty VARCHAR(255),
     term VARCHAR(50) NOT NULL,
     prerequisites VARCHAR(255),
     antirequisites VARCHAR(255),
     course_description TEXT,
     ger_category VARCHAR(50),
     school VARCHAR(50) NOT NULL
 );
 
 CREATE TABLE students (
    e_id VARCHAR(50) PRIMARY KEY,
    s_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    pwd VARCHAR(100) NOT NULL,
    programme VARCHAR(100) NOT NULL,
    major VARCHAR(100) NOT NULL,
    minor VARCHAR(100)
);

CREATE TABLE schedule_g (
    course_code VARCHAR(50),
    section INT NOT NULL,
    csd DATE,
    ced DATE,
    d VARCHAR(20) NOT NULL,
    st VARCHAR(20) NOT NULL,
    et VARCHAR(20) NOT NULL
    

);

CREATE TABLE major_requirement (
    course_name VARCHAR(255),
    category ENUM('MAJOR', 'CORE', 'ELECTIVE')
);

INSERT INTO major_requirement (course_name, category) VALUES
-- MAJOR 
('ENR106 Introduction to Programming', 'MAJOR'),
('ENR107 Digital Electronics and Microprocessors', 'MAJOR'),
('ENR207 Electrical and Magnetic Circuits', 'MAJOR'),
('ENR208 Engineering Thermodynamics', 'MAJOR'),
('ENR302 Engineering Costing', 'MAJOR'),
('ENR108 Materials and the Engineering World', 'MAJOR'),
('ENR209 Mechanics of Rigid Bodies', 'MAJOR'),
('ENR210 Continuum Mechanics', 'MAJOR'),
('ENR110 Differential Equations in Engineering', 'MAJOR'),
('ENR111 Statistics for Engineers', 'MAJOR'),
('ENR112 Linear Algebra Laboratory', 'MAJOR'),
('ENR104 Engineering Visualisation and Drawings', 'MAJOR'),
('ENR105 Product Dissection and Realisation', 'MAJOR'),
('ENR215 Design, Innovation and Making', 'MAJOR'),
('ENR206 Sensors, Instruments and Experimentation', 'MAJOR'),
('ENR307 Communication III: Technical Communication', 'MAJOR'),
-- CORE 
('CSE103 Elements of Computer Science and Engineering', 'CORE'),
('CSE203 Object Oriented Programming', 'CORE'),
('CSE211 Discrete Mathematics', 'CORE'),
('CSE305 Data Structures', 'CORE'),
('CSE400 Fundamentals of Probability in Computing', 'CORE'),
('CSE210 Digital Logic with Hardware Description Language', 'CORE'),
('CSE401 Database Management System', 'CORE'),
('CSE302 Computer Organisation and Architecture', 'CORE'),
('CSE301 Design and Analysis of Algorithms', 'CORE'),
('CSE402 Systems Programming', 'CORE'),
('CSE403 Introduction to Embedded Systems', 'CORE'),
('CSE404 Operating Systems', 'CORE'),
('CSE405 Computer Networks', 'CORE'),
('CSE406 Theory of Computing', 'CORE'),
('CSE547 Artificial Intelligence', 'CORE'),
('CSE407 Software Engineering', 'CORE'),
-- ELECTIVES
('Advanced Computer Arithmetic: Algorithms and Subsystems', 'ELECTIVE'),
('Artificial Intelligence', 'ELECTIVE'),
('Big Data Analytics', 'ELECTIVE'),
('Cloud Computing', 'ELECTIVE'),
('Computer Vision', 'ELECTIVE'),
('Human Computer Interactions', 'ELECTIVE'),
('Integrated Circuit Devices and Fabrication Technology', 'ELECTIVE'),
('Internet of Things', 'ELECTIVE'),
('Introduction to Blockchain Technologies, Applications and Research', 'ELECTIVE'),
('Parallel and Distributed Systems', 'ELECTIVE'),
('Probabilistic Graphical Models', 'ELECTIVE'),
('Social Network Analysis', 'ELECTIVE'),
('VLSI Design', 'ELECTIVE'),
('Wireless Communication', 'ELECTIVE');
CREATE TABLE taken_c (
    e_id VARCHAR(50),
    course_code VARCHAR(50),
    
    FOREIGN KEY (e_id) REFERENCES students(e_id)
    
);

CREATE TABLE c_planned (
    e_id VARCHAR(50),
    course_code VARCHAR(50),
    
    FOREIGN KEY (e_id) REFERENCES students(e_id),
    FOREIGN KEY (course_code) REFERENCES courses(course_code)
);


-- RUN TESTS
show tables;
select * from students;
select * from course;
select * from schedule_g;
select * from major_requirement;
select * from taken_c;
CREATE 
(SELECT:TOPIC{name:"SELECT",basic_def:"Retrieves data from a table.",syntax:"SELECT column1, column2, FROM table_name;",example_1:"SELECT CustomerName, City FROM Customers;",example_1_desc:"Retrieve customer name and city of all customer from the Customer data table"}),
(INSERT:TOPIC{name:"INSERT",basic_def:"Inserts new data into a table.",syntax_1:"INSERT INTO table_name (column1, column2, column3, ...) VALUES (value1, value2, value3, ...);",syntax_2:"INSERT INTO table_name VALUES (value1, value2, value3, ...);",example_1:"INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country) VALUES ('Cardinal', 'Tom B. Erichsen', 'Skagen 21', 'Stavanger', '4006', 'Norway');",example_1_desc:"Insert data into the table "}),


(DDL:SQL_COMMAND{name:"DDL",expansion:"Data Definition Language.",definition:"DDL is an abbreviation for Data Definition Language. It is concerned with database schemas and descriptions of how data should be stored in the database. DDL statements are auto-committed, meaning the changes are immediately made to the database and cannot be rolled back. These commands enable database administrators and developers to manage and optimize MySQL databases effectively."}),
(DML:SQL_COMMAND{name:"DML",expansion:"Data Manipulation Language",definition:"DML stands for Data Manipulation Language. It deals with data manipulation and includes the most common SQL statements such as SELECT, INSERT, UPDATE, DELETE, etc. DML statements are not auto-committed, meaning the changes can be rolled back if necessary. By mastering these DML commands, you can efficiently manipulate data in MySQL databases."}),
(DCL:SQL_COMMAND{name:"DCL",expansion:"Data Control Language",definition:"DCL stands for Data Control Language. It includes commands such as GRANT and is primarily concerned with rights, permissions, and other controls of the database system. DCL statements are also auto-committed."}),
(TCL:SQL_COMMAND{name:"TCL",expansion:"Transaction Control Language",definition:"TCL stands for Transaction Control Language. It deals with transactions within a database, which are groups of related DML statements treated as a single unit."}),

(SELECT)-[:Topic_of]-> (DDL),
(INSERT)-[:Topic_of]-> (DDL);



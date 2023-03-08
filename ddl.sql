CREATE TABLE t_todo (
	id INT auto_increment NOT NULL,
	task varchar(30) NOT NULL,
	status TINYINT DEFAULT 0 NOT NULL,
	created_by varchar(30) NOT NULL,
	created_date TIMESTAMP NOT NULL,
	last_modified_by varchar(30) NULL,
	last_modified_date TIMESTAMP NULL,
	CONSTRAINT t_todo_PK PRIMARY KEY (id)
);
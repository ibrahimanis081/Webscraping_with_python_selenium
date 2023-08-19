CREATE TABLE IF NOT EXISTS us_accredited_online_colleges(
    `serial_no` INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
    `school_name` VARCHAR(50),
    `tuition` BIGINT,
    `location` VARCHAR(30),
    `state` VARCHAR(30),
    `degree_1` VARCHAR(30),
    `degree_2` VARCHAR(30),
    `degree_3` VARCHAR(30),
    `degree_4` VARCHAR(30),
    `degree_5` VARCHAR(30),
    `degree_6` VARCHAR(30),
    `degree_7` VARCHAR(30),
    `school_type` VARCHAR(30),
    `duration` VARCHAR(30)
);
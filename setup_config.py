setup_config={
    "tables":{
        "homework":"""
            CREATE TABLE IF NOT EXISTS homework (
            id INT(10) UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
            updated_utc TIMESTAMP DEFAULT(UTC_TIMESTAMP),
            childid INT(10) UNSIGNED NOT NULL,
            firstname VARCHAR(255),
            homework JSON)""",

        "weekplan":"""
            CREATE TABLE IF NOT EXISTS weekplan (
            id INT(10) UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
            updated_utc TIMESTAMP DEFAULT(UTC_TIMESTAMP),
            childid INT(10) UNSIGNED NOT NULL,
            firstname VARCHAR(255),
            weekplan JSON)""",
    }
}

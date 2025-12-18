
CREATE DATABASE IF NOT EXISTS CRMS;
USE CRMS;

-- 1. Table: crime_categories
CREATE TABLE crime_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    severity VARCHAR(20),
    description TEXT,
    typical_punishment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Table: officers
CREATE TABLE officers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    badge_number VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    officer_rank VARCHAR(50),
    department VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(120),
    station VARCHAR(100),
    join_date DATE,
    officer_status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Table: suspects
CREATE TABLE suspects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    alias VARCHAR(120),
    age INT,
    gender VARCHAR(10),
    address TEXT,
    phone VARCHAR(15),
    identification_marks TEXT,
    criminal_history TEXT,
    photo_url VARCHAR(255),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Table: reports
CREATE TABLE reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reporter VARCHAR(120) NOT NULL,
    suspect VARCHAR(120),
    crime VARCHAR(160),
    status ENUM('Filed', 'Investigating', 'Closed') DEFAULT 'Filed',
    location VARCHAR(160),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE evidence (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_id INT NOT NULL,
    evidence_type VARCHAR(50),
    description TEXT,
    collected_by VARCHAR(120),
    collection_date DATE,
    location_found VARCHAR(200),
    file_path VARCHAR(255),
    status VARCHAR(30),
    evidence_number VARCHAR(100) UNIQUE,
    case_number VARCHAR(100),
    storage_location VARCHAR(255),
    chain_of_custody TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_report_evidence 
    FOREIGN KEY (report_id) REFERENCES reports(id) 
    ON DELETE CASCADE ON UPDATE CASCADE
);

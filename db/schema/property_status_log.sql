CREATE TABLE property_status_log (
    id INT AUTO_INCREMENT PRIMARY KEY,

    property_id INT NOT NULL,
    old_status ENUM('draft','active','sold','rented'),
    new_status ENUM('draft','active','sold','rented'),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (property_id) REFERENCES properties(id)
        ON DELETE CASCADE
);

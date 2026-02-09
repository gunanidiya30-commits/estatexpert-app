CREATE TABLE price_history (
    id INT AUTO_INCREMENT PRIMARY KEY,

    property_id INT NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (property_id) REFERENCES properties(id)
        ON DELETE CASCADE
);

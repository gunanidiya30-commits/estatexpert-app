CREATE TABLE properties (
    id INT AUTO_INCREMENT PRIMARY KEY,

    title VARCHAR(200) NOT NULL,
    description TEXT,

    property_type ENUM('apartment','villa','plot','commercial') NOT NULL,
    bhk INT,
    area_sqft INT,

    city VARCHAR(100),
    locality VARCHAR(100),

    price DECIMAL(12,2) NOT NULL,

    status ENUM('draft','active','sold','rented') DEFAULT 'draft',

    owner_id INT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (owner_id) REFERENCES users(id)
);

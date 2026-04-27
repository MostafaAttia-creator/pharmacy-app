
CREATE TABLE Medicines (
    Med_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Category TEXT,
    Price REAL CHECK (Price > 0),
    Quantity INTEGER DEFAULT 0 CHECK (Quantity >= 0),
    Expiry_Date TEXT
);

-- TABLE: Customers
CREATE TABLE Customers (
    Customer_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Phone TEXT
);

-- TABLE: Suppliers
CREATE TABLE Suppliers (
    Supplier_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Phone TEXT
);

-- TABLE: Sales
CREATE TABLE Sales (
    Sale_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Customer_ID INTEGER,
    Sales_Date TEXT DEFAULT CURRENT_TIMESTAMP,
    Total_Amount REAL,

    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID)
);

-- TABLE: Sale_Details
CREATE TABLE Sale_Details (
    Sale_ID INTEGER,
    Med_ID INTEGER,
    Quantity INTEGER CHECK (Quantity > 0),
    Price REAL,

    PRIMARY KEY (Sale_ID, Med_ID),

    FOREIGN KEY (Sale_ID) REFERENCES Sales(Sale_ID),
    FOREIGN KEY (Med_ID) REFERENCES Medicines(Med_ID)
);

-- =========================
-- TRIGGER (SQLite version)
-- =========================

CREATE TRIGGER trg_DecreaseStock
AFTER INSERT ON Sale_Details
BEGIN
    UPDATE Medicines
    SET Quantity = Quantity - NEW.Quantity
    WHERE Med_ID = NEW.Med_ID;
END;

CREATE TRIGGER IF NOT EXISTS trg_DecreaseStock
AFTER INSERT ON Sale_Details
BEGIN
    UPDATE Medicines
    SET Quantity = Quantity - NEW.Quantity
    WHERE Med_ID = NEW.Med_ID;
END;

-- =========================
-- SAMPLE DATA (Customers)
-- =========================

INSERT INTO Customers (Name, Phone) VALUES
('Ahmed Ali', '01012345678'),
('Mohamed Hassan', '01123456789'),
('Omar Khaled', '01234567890'),
('Mahmoud Tarek', '01098765432'),
('Youssef Adel', '01187654321'),
('Kareem Reda', '01211223344'),
('Ali Mostafa', '01055667788'),
('Ibrahim Nasser', '01166778899'),
('Hossam Fathy', '01277889900'),
('Tamer Magdy', '01022334455'),
('Mostafa Samir', '01133445566'),
('Wael Hamdy', '01244556677'),
('Sherif Ahmed', '01099887766'),
('Amr Saad', '01188776655'),
('Khaled Fawzy', '01277665544'),
('Hany Salah', '01066554433'),
('Sayed Mahmoud', '01155443322'),
('Essam Gaber', '01244332211'),
('Adel Farouk', '01033221100'),
('Sameh Younes', '01122110099');

-- =========================
-- SAMPLE DATA (Medicines)
-- =========================

INSERT INTO Medicines (Name, Category, Price, Quantity, Expiry_Date) VALUES
('Panadol', 'Painkiller', 20, 100, '2027-05-01'),
('Brufen', 'Painkiller', 30, 80, '2026-12-15'),
('Cataflam', 'Painkiller', 35, 70, '2026-09-05'),
('Aspirin', 'Painkiller', 18, 120, '2027-08-15'),
('Dolo-D', 'Painkiller', 27, 95, '2027-01-25'),
('Augmentin', 'Antibiotic', 75, 50, '2026-08-20'),
('Amoxicillin', 'Antibiotic', 40, 60, '2027-01-10'),
('Flagyl', 'Antibiotic', 45, 65, '2027-02-14'),
('Zithromax', 'Antibiotic', 90, 30, '2026-11-10'),
('Ciprofloxacin', 'Antibiotic', 55, 45, '2027-06-01'),
('Zyrtec', 'Allergy', 25, 90, '2027-03-18'),
('Claritine', 'Allergy', 28, 85, '2026-11-30'),
('Telfast', 'Allergy', 48, 60, '2026-10-05'),
('Allerid', 'Allergy', 22, 75, '2027-04-12'),
('Histazine', 'Allergy', 20, 80, '2026-12-20'),
('Ventolin', 'Respiratory', 60, 40, '2027-06-12'),
('Bricanyl', 'Respiratory', 65, 35, '2026-09-30'),
('Pulmicort', 'Respiratory', 110, 25, '2027-02-22'),
('Seretide', 'Respiratory', 150, 20, '2026-12-05'),
('Atrovent', 'Respiratory', 70, 30, '2027-03-01'),
('Otrivin', 'Nasal Spray', 22, 75, '2026-10-22'),
('Nazacort', 'Nasal Spray', 45, 40, '2027-07-15'),
('Flixonase', 'Nasal Spray', 55, 35, '2026-11-11'),
('Rhinocort', 'Nasal Spray', 50, 30, '2027-05-20'),
('Nasonex', 'Nasal Spray', 65, 25, '2026-12-25'),
('Insulin', 'Diabetes', 150, 30, '2026-07-01'),
('Glucophage', 'Diabetes', 55, 55, '2027-04-09'),
('Diamicron', 'Diabetes', 70, 40, '2026-10-10'),
('Amaryl', 'Diabetes', 65, 45, '2027-01-30'),
('Januvia', 'Diabetes', 200, 20, '2026-09-15'),
('Concor', 'Heart', 70, 45, '2026-12-01'),
('Atenolol', 'Heart', 35, 60, '2027-03-25'),
('Bisoprolol', 'Heart', 50, 50, '2026-11-18'),
('Plavix', 'Heart', 120, 25, '2027-06-10'),
('Lipitor', 'Heart', 95, 30, '2026-08-05'),
('Vitamin C', 'Supplement', 15, 150, '2027-09-10'),
('Omega 3', 'Supplement', 65, 50, '2026-11-11'),
('Calcium D', 'Supplement', 40, 80, '2027-02-28'),
('Multivitamin', 'Supplement', 35, 90, '2026-12-12'),
('Zinc', 'Supplement', 25, 100, '2027-05-05'),
('Nexium', 'Stomach', 85, 35, '2027-02-20'),
('Omeprazole', 'Stomach', 30, 70, '2026-10-01'),
('Antinal', 'Antidiarrheal', 32, 70, '2026-09-17'),
('Imodium', 'Antidiarrheal', 45, 50, '2027-03-03'),
('Buscopan', 'Antispasmodic', 38, 60, '2026-12-08'),
('Doliprane', 'Painkiller', 22, 85, '2027-01-15'),
('Ketofan', 'Painkiller', 33, 65, '2026-11-27'),
('SpasmoDigestin', 'Digestive', 28, 75, '2027-04-18'),
('Digestin', 'Digestive', 26, 80, '2026-09-09'),
('Coloverin', 'Digestive', 42, 55, '2027-06-25');

-- =========================
-- SAMPLE DATA (Suppliers)
-- =========================

INSERT INTO Suppliers (Name, Phone) VALUES
('El Ezaby Pharma', '01011112222'),
('Seif Pharmacies Supply', '01122223333'),
('Rameda Distribution', '01233334444'),
('Eva Pharma Supply', '01044445555'),
('Amoun Pharma', '01155556666'),
('Pharco Distribution', '01266667777'),
('EIPICO Supply', '01077778888'),
('Global Pharma Trade', '01188889999'),
('Delta Medical Supply', '01299990000'),
('Cairo Drug Store', '01012121212'),
('Nile Pharma Group', '01123232323'),
('Future Medical', '01234343434'),
('United Pharma', '01045454545'),
('Advanced Healthcare', '01156565656'),
('Al Shifa Supply', '01267676767');
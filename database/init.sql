CREATE DATABASE TODOAPP;

BEGIN
    USE TODOAPP;

    CREATE TABLE Users (
        UserID INT IDENTITY(1,1) PRIMARY KEY,
        UserName NVARCHAR(50) NOT NULL,
        Email NVARCHAR(100) UNIQUE NOT NULL,
        Password NVARCHAR(255) NOT NULL,
        Name NVARCHAR(50) NULL,
        DateOfBirth DATE NULL,
        IsActive BIT DEFAULT 1
    );

    CREATE TABLE TaskStatus (
        StatusID INT IDENTITY(1,1) PRIMARY KEY,
        Name NVARCHAR(50) NOT NULL UNIQUE,
        Description NVARCHAR(255)
    );

    CREATE TABLE Categories (
        CategoryID INT IDENTITY(1,1) PRIMARY KEY,
        Name NVARCHAR(50) NOT NULL UNIQUE,
        Description NVARCHAR(255)
    );

    CREATE TABLE Tasks (
        TaskID INT IDENTITY(1,1) PRIMARY KEY,
        UserID INT NOT NULL,
        Title NVARCHAR(255) NOT NULL,
        Description NVARCHAR(MAX),
        Notes NVARCHAR(MAX),
        DueDate DATETIME,
        IsCompleted BIT DEFAULT 0,
        Priority TINYINT DEFAULT 0,
        CategoryID INT NOT NULL,
        StatusID INT NOT NULL,
        CONSTRAINT FK_Tasks_Users FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
        CONSTRAINT FK_Tasks_Categories FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID) ON DELETE CASCADE,
        CONSTRAINT FK_Tasks_TaskStatus FOREIGN KEY (StatusID) REFERENCES TaskStatus(StatusID) ON DELETE CASCADE
    );

    INSERT INTO TaskStatus (Name, Description)
    VALUES 
    ('Pending', 'Task is pending and not started yet'),
    ('In Progress', 'Task is currently being worked on'),
    ('Completed', 'Task has been completed'),
    ('On Hold', 'Task is temporarily paused'),
    ('Cancelled', 'Task has been cancelled');

    INSERT INTO Categories (Name, Description)
    VALUES 
    ('Work', 'Tasks related to work or professional activities'),
    ('Personal', 'Tasks related to personal activities or goals'),
    ('Family', 'Tasks related to family responsibilities'),
    ('Others', 'Miscellaneous tasks not fitting into the above categories');

    INSERT INTO Users (UserName, Email, Password, Name, DateOfBirth)
    VALUES 
    ('john_doe', 'john.doe@example.com', 'hashed_password_1', 'John Doe', '1985-06-15'),
    ('jane_smith', 'jane.smith@example.com', 'hashed_password_2', 'Jane Smith', '1990-02-20'),
    ('alice_wonder', 'alice.wonder@example.com', 'hashed_password_3', 'Alice Wonder', '1988-11-05');

    -- Insert into Tasks
    INSERT INTO Tasks (UserID, Title, Description, Notes, DueDate, IsCompleted, Priority, CategoryID, StatusID)
    VALUES 
    (1, 'Complete project report', 'Prepare the final report for Q4 project.', 'Include financial analysis section and review by Tuesday.', '2025-01-15', 0, 2, 1, 2), -- Work, In Progress
    (1, 'Buy groceries', 'Get fruits, vegetables, and milk from the store.', 'Check for any discounts or offers.', '2025-01-12', 0, 1, 2, 1), -- Personal, Pending
    (2, 'Plan family vacation', 'Research vacation destinations for the family summer trip.', NULL, '2025-03-01', 0, 0, 3, 1), -- Family, Pending
    (3, 'Organize bookshelf', 'Sort books by genre and clean the shelves.', NULL, '2025-01-18', 0, 1, 2, 1), -- Personal, Pending
    (2, 'Team meeting', 'Discuss project timelines and deliverables with the team.', 'Prepare slides for presentation.', '2025-01-14', 0, 2, 1, 2); -- Work, In Progress
END

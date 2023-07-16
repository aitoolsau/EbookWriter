ALTER TABLE projects
ADD COLUMN Task VARCHAR(255),
ADD COLUMN Topic VARCHAR(255),
ADD COLUMN Style VARCHAR(255),
ADD COLUMN Audience VARCHAR(255),
ADD COLUMN Length VARCHAR(255),
ADD COLUMN Format VARCHAR(255),
ADD COLUMN AdditionalInformation TEXT;
ALTER TABLE projects
DROP COLUMN Task,
DROP COLUMN Topic,
DROP COLUMN Style,
DROP COLUMN Audience,
DROP COLUMN Length,
DROP COLUMN Format,
DROP COLUMN AdditionalInformation;
CREATE TABLE writers (
    WriterID INT AUTO_INCREMENT,
    UserID INT NOT NULL,
    Task VARCHAR(255),
    Topic VARCHAR(255),
    Style VARCHAR(255),
    Audience VARCHAR(255),
    Length VARCHAR(255),
    Format VARCHAR(255),
    AdditionalInformation TEXT,
    PRIMARY KEY (WriterID),
    FOREIGN KEY (UserID) REFERENCES users(UserID)
);
CREATE TABLE writers (
    WriterID INT AUTO_INCREMENT,
    UserID INT NOT NULL,
    Task VARCHAR(255),
    Topic VARCHAR(255),
    Style VARCHAR(255),
    Audience VARCHAR(255),
    Length VARCHAR(255),
    Format VARCHAR(255),
    AdditionalInformation TEXT,
    PRIMARY KEY (WriterID),
    FOREIGN KEY (UserID) REFERENCES users(UserID)
);
CREATE TABLE writers (
    WriterID INT AUTO_INCREMENT,
    UserID INT NOT NULL,
    Task VARCHAR(255),
    Topic VARCHAR(255),
    Style VARCHAR(255),
    Audience VARCHAR(255),
    Length VARCHAR(255),
    Format VARCHAR(255),
    AdditionalInformation TEXT,
    PRIMARY KEY (WriterID),
    FOREIGN KEY (UserID) REFERENCES users(UserID)
);
ALTER TABLE writers
ADD CONSTRAINT fk_userid
FOREIGN KEY (UserID) REFERENCES users(UserID);

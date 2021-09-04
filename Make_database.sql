-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema AnimalShelterMS
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `AnimalShelterMS` ;

-- -----------------------------------------------------
-- Schema AnimalShelterMS
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `AnimalShelterMS` DEFAULT CHARACTER SET utf8 ;
USE `AnimalShelterMS` ;

-- -----------------------------------------------------
-- Table `AnimalShelterMS`.`Person`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AnimalShelterMS`.`Person` ;

CREATE TABLE IF NOT EXISTS `AnimalShelterMS`.`Person` (
  `PersonID` INT NOT NULL AUTO_INCREMENT,
  `Email` VARCHAR(45) NULL,
  `Phone` CHAR(10) NULL,
  `Address` VARCHAR(45) NULL,
  `Verified` TINYINT NULL,
  `FirstName` CHAR(20) NOT NULL,
  `LastName` CHAR(20) NULL,
  PRIMARY KEY (`PersonID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AnimalShelterMS`.`Employee`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AnimalShelterMS`.`Employee` ;

CREATE TABLE IF NOT EXISTS `AnimalShelterMS`.`Employee` (
  `WorkerID` INT NOT NULL AUTO_INCREMENT,
  `SeniorID` INT NULL,
  `PersonID` INT NOT NULL,
  `Salary` DECIMAL NULL,
  `CompanyEmail` CHAR(20) NOT NULL,
  PRIMARY KEY (`WorkerID`, `PersonID`),
  INDEX `personID_idx` (`PersonID` ASC) VISIBLE,
  INDEX `SeniorID_idx` (`SeniorID` ASC) VISIBLE,
  CONSTRAINT `EmployeeIsPerson`
    FOREIGN KEY (`PersonID`)
    REFERENCES `AnimalShelterMS`.`Person` (`PersonID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `SeniorIsEmployee`
    FOREIGN KEY (`SeniorID`)
    REFERENCES `AnimalShelterMS`.`Employee` (`PersonID`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AnimalShelterMS`.`Animal`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AnimalShelterMS`.`Animal` ;

CREATE TABLE IF NOT EXISTS `AnimalShelterMS`.`Animal` (
  `AnimalID` INT NOT NULL AUTO_INCREMENT,
  `Name` CHAR(20) NULL,
  `DateOfBirth` DATE NULL,
  `Gender` CHAR(1) NULL,
  `Breed` CHAR(20) NULL,
  `Weight` DECIMAL NULL,
  `Healthy` TINYINT NULL,
  `AdoptionInProgress` TINYINT NULL,
  PRIMARY KEY (`AnimalID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AnimalShelterMS`.`Vet`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AnimalShelterMS`.`Vet` ;

CREATE TABLE IF NOT EXISTS `AnimalShelterMS`.`Vet` (
  `VetID` INT NOT NULL AUTO_INCREMENT,
  `RegNo` INT NOT NULL,
  `OfficeContact` VARCHAR(45) NULL,
  `PersonID` INT NOT NULL,
  PRIMARY KEY (`VetID`, `PersonID`),
  INDEX `PersonID_idx` (`PersonID` ASC) VISIBLE,
  CONSTRAINT `VetIsPerson`
    FOREIGN KEY (`PersonID`)
    REFERENCES `AnimalShelterMS`.`Person` (`PersonID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AnimalShelterMS`.`MedicalRecords`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AnimalShelterMS`.`MedicalRecords` ;

CREATE TABLE IF NOT EXISTS `AnimalShelterMS`.`MedicalRecords` (
  `RecordID` INT NOT NULL AUTO_INCREMENT,
  `AnimalID` INT NULL,
  `VetID` INT NULL,
  `Time` DATETIME NOT NULL,
  `Comments` CHAR(100),
  `TypeOfVisit` CHAR(30) NOT NULL,
  `Healthy` TINYINT NOT NULL,
  INDEX `VetID_idx` (`VetID` ASC) VISIBLE,
  PRIMARY KEY (`RecordID`),
  UNIQUE INDEX `RecordID_UNIQUE` (`RecordID` ASC) VISIBLE,
  INDEX `OfAnimal_idx` (`AnimalID` ASC) VISIBLE,
  CONSTRAINT `OfAnimal`
    FOREIGN KEY (`AnimalID`)
    REFERENCES `AnimalShelterMS`.`Animal` (`AnimalID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `ByVet`
    FOREIGN KEY (`VetID`)
    REFERENCES `AnimalShelterMS`.`Vet` (`VetID`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AnimalShelterMS`.`Adoptions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AnimalShelterMS`.`Adoptions` ;

CREATE TABLE IF NOT EXISTS `AnimalShelterMS`.`Adoptions` (
  `PersonID` INT NOT NULL,
  `AnimalID` INT NOT NULL,
  `DateOfAdoption` DATETIME NOT NULL,
  `Overseer` INT NULL,
  `DateInitiated` DATETIME NULL,
  `AdoptionID` INT NOT NULL,
  PRIMARY KEY (`AdoptionID`, `PersonID`, `AnimalID`),
  INDEX `AnimalID_idx` (`AnimalID` ASC) VISIBLE,
  INDEX `OverseerID_idx` (`Overseer` ASC) VISIBLE,
  CONSTRAINT `ByPerson`
    FOREIGN KEY (`PersonID`)
    REFERENCES `AnimalShelterMS`.`Person` (`PersonID`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT `AnimalAdopted`
    FOREIGN KEY (`AnimalID`)
    REFERENCES `AnimalShelterMS`.`Animal` (`AnimalID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `OverseenByEmpl`
    FOREIGN KEY (`Overseer`)
    REFERENCES `AnimalShelterMS`.`Employee` (`WorkerID`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AnimalShelterMS`.`DailyTasks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AnimalShelterMS`.`DailyTasks` ;

CREATE TABLE IF NOT EXISTS `AnimalShelterMS`.`DailyTasks` (
  `AnimalID` INT NOT NULL,
  `WorkerID` INT NOT NULL,
  `Task` INT NOT NULL AUTO_INCREMENT,
  `Description` CHAR(30) NULL,
  PRIMARY KEY (`Task`),
  INDEX `WorkerID_idx` (`WorkerID` ASC) VISIBLE,
  CONSTRAINT `TaskForAnimal`
    FOREIGN KEY (`AnimalID`)
    REFERENCES `AnimalShelterMS`.`Animal` (`AnimalID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `TaskOfEmployee`
    FOREIGN KEY (`WorkerID`)
    REFERENCES `AnimalShelterMS`.`Employee` (`WorkerID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

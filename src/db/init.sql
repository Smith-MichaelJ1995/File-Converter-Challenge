CREATE DATABASE files;
USE files;

-- MySQL dump 10.13  Distrib 8.0.29, for macos12 (arm64)
--
-- Host: localhost    Database: intel
-- ------------------------------------------------------
-- Server version	8.0.29

--
-- Table structure for table `PDF` files
DROP TABLE IF EXISTS `PDF`;

CREATE TABLE PDF (
  id INT primary key NOT NULL AUTO_INCREMENT UNIQUE,
  filename VARCHAR(255),
  createdAt VARCHAR(255),
  createdBy VARCHAR(255),
  docType ENUM ('Financial', "Events", "eRegulatory")
);
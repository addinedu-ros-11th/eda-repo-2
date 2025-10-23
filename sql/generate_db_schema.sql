-- MySQL dump 10.13  Distrib 8.0.43, for Linux (x86_64)
--
-- Host: edu-1.cpoiow8a8io6.ap-northeast-2.rds.amazonaws.com    Database: EDA_PROJECT
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `boxoffice`
--

DROP TABLE IF EXISTS `boxoffice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `boxoffice` (
  `movie_name` varchar(36) COLLATE utf8mb4_general_ci NOT NULL,
  `release_date` date NOT NULL,
  `date` date NOT NULL,
  `region` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `income` bigint DEFAULT NULL,
  `views` int DEFAULT NULL,
  `screen` int DEFAULT NULL,
  `play_count` int DEFAULT NULL,
  `is_korean` char(1) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`movie_name`,`release_date`,`date`,`region`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `incheon_airport`
--

DROP TABLE IF EXISTS `incheon_airport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `incheon_airport` (
  `date` date NOT NULL,
  `destination` varchar(32) NOT NULL,
  `airline` varchar(32) NOT NULL,
  `dep_flight` int DEFAULT NULL,
  `arr_flight` int DEFAULT NULL,
  `dep_psg` int DEFAULT NULL,
  `arr_psg` int DEFAULT NULL,
  PRIMARY KEY (`date`,`destination`,`airline`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `n_sp_category`
--

DROP TABLE IF EXISTS `n_sp_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `n_sp_category` (
  `cat_id` int NOT NULL,
  `parent_id` int DEFAULT NULL,
  `title` varchar(32) DEFAULT NULL,
  `level` int DEFAULT NULL,
  PRIMARY KEY (`cat_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `n_sp_trend`
--

DROP TABLE IF EXISTS `n_sp_trend`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `n_sp_trend` (
  `date` date NOT NULL,
  `cat_id` int NOT NULL,
  `ratio` float DEFAULT NULL,
  PRIMARY KEY (`date`,`cat_id`),
  KEY `FK_n_sp_category_TO_n_sp_trend_1` (`cat_id`),
  CONSTRAINT `FK_n_sp_category_TO_n_sp_trend_1` FOREIGN KEY (`cat_id`) REFERENCES `n_sp_category` (`cat_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seoul_airenv`
--

DROP TABLE IF EXISTS `seoul_airenv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seoul_airenv` (
  `date` date NOT NULL,
  `hour` int NOT NULL,
  `region` varchar(32) NOT NULL,
  `dust` float DEFAULT NULL,
  PRIMARY KEY (`date`,`hour`,`region`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seoul_daily_population`
--

DROP TABLE IF EXISTS `seoul_daily_population`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seoul_daily_population` (
  `date` date NOT NULL,
  `gu_id` int NOT NULL,
  `avg_pop` float DEFAULT NULL,
  `max_pop` int DEFAULT NULL,
  `min_pop` int DEFAULT NULL,
  `day_pop` int DEFAULT NULL,
  `night_pop` int DEFAULT NULL,
  `gu_name` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`date`,`gu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seoul_time_population`
--

DROP TABLE IF EXISTS `seoul_time_population`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seoul_time_population` (
  `sex` char(1) NOT NULL,
  `age` int NOT NULL,
  `hour` int NOT NULL,
  `date` date NOT NULL,
  `gu_id` int NOT NULL,
  `gu_name` varchar(32) DEFAULT NULL,
  `population` int DEFAULT NULL,
  PRIMARY KEY (`sex`,`age`,`hour`,`date`,`gu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seoul_time_total_population`
--

DROP TABLE IF EXISTS `seoul_time_total_population`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seoul_time_total_population` (
  `hour` int NOT NULL,
  `date` date NOT NULL,
  `gu_id` int NOT NULL,
  `population` int DEFAULT NULL,
  PRIMARY KEY (`hour`,`date`,`gu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seoul_weather`
--

DROP TABLE IF EXISTS `seoul_weather`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seoul_weather` (
  `date` date NOT NULL,
  `rain` float DEFAULT NULL,
  `wind_spd` float DEFAULT NULL,
  `wind_dir` int DEFAULT NULL,
  `Field` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `traffic_gate`
--

DROP TABLE IF EXISTS `traffic_gate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `traffic_gate` (
  `date` date NOT NULL,
  `hour` int NOT NULL,
  `gate` varchar(32) NOT NULL,
  `in_traffic` int DEFAULT NULL,
  `out_traffic` int DEFAULT NULL,
  PRIMARY KEY (`date`,`hour`,`gate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `traffic_region`
--

DROP TABLE IF EXISTS `traffic_region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `traffic_region` (
  `date` date NOT NULL,
  `hour` int NOT NULL,
  `region` varchar(32) NOT NULL,
  `in_traffic` int DEFAULT NULL,
  `out_traffic` int DEFAULT NULL,
  PRIMARY KEY (`date`,`hour`,`region`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-23 16:12:27

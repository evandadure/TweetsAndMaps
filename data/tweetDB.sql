SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+01:00";

--
-- Base de données :  `isoc_tp_twitter`
--

-- --------------------------------------------------------
DROP TABLE IF EXISTS `keyword`;
DROP TABLE IF EXISTS `tweet`;
DROP TABLE IF EXISTS `city`;
DROP TABLE IF EXISTS `word`;


CREATE TABLE `tweet` (
  `id_tweet` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NULL DEFAULT NULL,
  `text` varchar(280) DEFAULT NULL,
  `user_id` varchar(280) DEFAULT NULL,
  `user_name` varchar(280) DEFAULT NULL,
  `screen_name` varchar(280) DEFAULT NULL,
  `latitude` varchar(280) DEFAULT NULL,
  `longitude` varchar(280) DEFAULT NULL,
  `searched_keyword` varchar(280) DEFAULT NULL,
  `nearest_city` varchar(200) DEFAULT NULL,
  `numero_tweet` varchar(100) DEFAULT NULL,
  PRIMARY KEY (id_tweet)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Structure de la table `city`
--

CREATE TABLE `city` (
  `city_name` varchar(280) NOT NULL,
  PRIMARY KEY (city_name)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Structure de la table `word`
--

CREATE TABLE `word` (
  `label` varchar(280) NOT NULL,
  PRIMARY KEY (label)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Structure de la table `keyword`
--

CREATE TABLE `keyword` (
  `numero_tweet` varchar(100) NOT NULL,
  `city_name` varchar(280) NOT NULL,
  `label` varchar(280) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


ALTER TABLE keyword ADD PRIMARY KEY(numero_tweet,label,city_name);


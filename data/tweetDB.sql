SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+01:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `tp_twitterosm`
--

-- --------------------------------------------------------

DROP TABLE IF EXISTS city;
DROP TABLE IF EXISTS word;
DROP TABLE IF EXISTS tweet;
DROP TABLE IF EXISTS keyword;

--
-- Structure de la table `city`
--

CREATE TABLE `city` (
  `city_name` varchar(280) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Structure de la table `keyword`
--

CREATE TABLE `keyword` (
  `numero_tweet` varchar(100) NOT NULL,
  `city_name` varchar(280) NOT NULL,
  `label` varchar(280) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Structure de la table `tweet`
--

CREATE TABLE `tweet` (
  `numero_tweet` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `text` varchar(280) DEFAULT NULL,
  `user_id` varchar(280) DEFAULT NULL,
  `user_name` varchar(280) DEFAULT NULL,
  `screen_name` varchar(280) DEFAULT NULL,
  `latitude` varchar(280) DEFAULT NULL,
  `longitude` varchar(280) DEFAULT NULL,
  `searched_keyword` varchar(280) DEFAULT NULL,
  `nearest_city` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Structure de la table `word`
--

CREATE TABLE `word` (
  `label` varchar(280) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Index pour la table `city`
--
ALTER TABLE `city`
  ADD PRIMARY KEY (`city_name`);

--
-- Index pour la table `keyword`
--
ALTER TABLE `keyword`
  ADD PRIMARY KEY (`numero_tweet`,`label`,`city_name`);

--
-- Index pour la table `tweet`
--
ALTER TABLE `tweet`
  ADD PRIMARY KEY (`numero_tweet`);

--
-- Index pour la table `word`
--
ALTER TABLE `word`
  ADD PRIMARY KEY (`label`);

  
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;



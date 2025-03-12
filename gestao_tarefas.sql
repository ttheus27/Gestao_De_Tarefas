-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Tempo de geração: 12/03/2025 às 23:12
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `gestao_tarefas`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `tarefas_concluidas`
--

CREATE TABLE `tarefas_concluidas` (
  `id_tarf` int(5) DEFAULT NULL,
  `tarefa_concluida` varchar(30) DEFAULT NULL,
  `classe_tarf` char(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `tarefas_concluidas`
--

INSERT INTO `tarefas_concluidas` (`id_tarf`, `tarefa_concluida`, `classe_tarf`) VALUES
(5, 'teste5', 'casa'),
(5, 'teste5', 'casa'),
(5, 'teste5', 'casa'),
(6, 'teste10', 'casa'),
(2, 'teste2', 'casa'),
(17, 'teste', 'trabalho'),
(10, 'preparar apresentação ', 'trabalho'),
(20, 'Arrumar PC', 'trabalho'),
(30, 'Limpar chao', 'casa');

-- --------------------------------------------------------

--
-- Estrutura para tabela `tarefas_pendentes`
--

CREATE TABLE `tarefas_pendentes` (
  `id_tarefa` int(11) NOT NULL,
  `tarefa` varchar(30) NOT NULL,
  `classe` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `tarefas_pendentes`
--

INSERT INTO `tarefas_pendentes` (`id_tarefa`, `tarefa`, `classe`) VALUES
(9, 'Estudar para a prova de calcul', 'faculdade'),
(11, 'Limpar o chao', 'casa'),
(12, 'Lançar notas', 'trabalho'),
(14, 'Lançar notas', 'trabalho'),
(19, 'Limpar casa ', 'casa'),
(21, 'Organizar cama', 'casa'),
(22, 'Fazer atividade de matematica', 'faculdade'),
(23, 'Limpar chao da empresa', 'trabalho'),
(24, 'Limpar chao do quarto', 'trabalho'),
(26, 'Arrumar a cama', 'casa'),
(27, 'Limpar banheiro do quarto', 'casa');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `tarefas_pendentes`
--
ALTER TABLE `tarefas_pendentes`
  ADD PRIMARY KEY (`id_tarefa`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `tarefas_pendentes`
--
ALTER TABLE `tarefas_pendentes`
  MODIFY `id_tarefa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

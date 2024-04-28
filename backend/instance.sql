INSERT INTO USUARIO (matricula, nome, senha, usuario, cpf) VALUES
(1, 'John Doe', 'password123', 'johndoe', 1234567890),
(2, 'Jane Smith', 'password456', 'janesmith', 9876543210);

INSERT INTO DESENVOLVEDOR (id, id_rsa) VALUES
(1, 'key1'),
(2, 'key2');

INSERT INTO FUNCIONARIO (id, produtora_item1, produtora_item2) VALUES
(1, 10, 20),
(2, 30, 40);

INSERT INTO VPS (ip, root_senha, id_rsa) VALUES
('192.168.1.100', 'rootpass1', 'key1'),
('192.168.1.101', 'rootpass2', 'key2');

INSERT INTO MANUTENCAO (data, descricao, id_matricula) VALUES
(NOW(), 'Maintenance of server', 1),
(NOW(), 'Update security patches', 2);

INSERT INTO PAGINA_GERAL (user_id, observacoes) VALUES
(1, 'Observation about performance'),
(2, 'General feedback');

INSERT INTO INFO_PRODUTIVIDADE (data, id, lista_de_produtividade, id_funcionario) VALUES
(NOW(), 'P123', 'Task1, Task2', 1),
(NOW(), 'P124', 'Task3, Task4', 2);

INSERT INTO BANCO_DE_DADOS (id_banco, ip_interno, ip_externo, fk_user_id) VALUES
(1, '10.0.0.1', '131.103.20.160', 1),
(2, '10.0.0.2', '131.103.20.161', 2);

INSERT INTO DISPOSITIVOS (id_ext, thresholds, id, fk_banco_id) VALUES
(1, 75, 'Device1', 1),
(2, 85, 'Device2', 2);

INSERT INTO ALARME (data, tipo, fk_banco) VALUES
(NOW(), 'Fire', 1),
(NOW(), 'Intrusion', 2);

INSERT INTO CAMERA (id, ip, fk_banco_id) VALUES
(1, '192.168.100.1', 1),
(2, '192.168.100.2', 2);

INSERT INTO SENSOR (id, ip, unidade, fk_banco_id) VALUES
(1, '192.168.200.1', 'Temperature', 1),
(2, '192.168.200.2', 'Humidity', 2);
CREATE SEQUENCE campi_id_seq;

CREATE TABLE campi(
    id BIGINT NOT NULL default nextval('campi_id_seq'),
    sigla CHAR(5) NOT NULL
);

ALTER SEQUENCE campi_id_seq owned
	BY campi.id;

ALTER TABLE
    campi ADD PRIMARY KEY(id);
-- -- -- -- -- -- -- -- -- 
CREATE SEQUENCE jornada_trabalho_id_seq;

CREATE TABLE jornada_trabalho(
    id BIGINT NOT NULL default nextval('jornada_trabalho_id_seq'),
    nome VARCHAR(255) NOT NULL
);

ALTER SEQUENCE jornada_trabalho_id_seq owned
	BY jornada_trabalho.id;

ALTER TABLE
    jornada_trabalho ADD PRIMARY KEY(id);
-- -- -- -- -- -- -- -- -- 
CREATE SEQUENCE cargos_docente_id_seq;

CREATE TABLE cargos_docente(
    id BIGINT NOT NULL,
    cargo_id BIGINT NOT NULL default nextval('cargos_docente_id_seq'),
    docente_id BIGINT NOT NULL,
    setor_id BIGINT NOT NULL
);

ALTER SEQUENCE cargos_docente_id_seq owned
	BY cargos_docente.id;

ALTER TABLE
    cargos_docente ADD PRIMARY KEY(id);
-- -- -- -- -- -- -- -- -- 
CREATE SEQUENCE setores_id_seq;

CREATE TABLE setores(
    id BIGINT NOT NULL default nextval('setores_id_seq'),
    nome VARCHAR(255) NOT NULL,
    campus BIGINT NOT NULL,
    type CHAR(4) NOT NULL check(type in ('siap','suap'))
);

ALTER SEQUENCE setores_id_seq owned
	BY setores.id;

ALTER TABLE
    setores ADD PRIMARY KEY(id);
-- -- -- -- -- -- -- -- -- 
CREATE SEQUENCE cargos_id_seq;

CREATE TABLE cargos(
    id BIGINT NOT NULL default nextval('cargos_id_seq'),
    nome VARCHAR(255) NOT NULL,
    jornada_trabalho_id BIGINT NOT NULL,
    semanal BOOLEAN NOT NULL,
    dedicacao_exclusiva BOOLEAN NOT NULL
);

ALTER SEQUENCE cargos_id_seq owned
	BY cargos.id;

ALTER TABLE
    cargos ADD PRIMARY KEY(id);
-- -- -- -- -- -- -- -- -- 
CREATE SEQUENCE categorias_id_seq;

CREATE TABLE categorias(
    id BIGINT NOT NULL default nextval('categorias_id_seq'),
    nome VARCHAR(255) NOT NULL
);

ALTER SEQUENCE categorias_id_seq owned
	BY categorias.id;

ALTER TABLE
    categorias ADD PRIMARY KEY(id);
-- -- -- -- -- -- -- -- -- 
CREATE SEQUENCE servidores_id_seq;

CREATE TABLE servidores(
    id BIGINT NOT NULL default nextval('servidores_id_seq'),
    nome VARCHAR(255) NOT NULL,
    matricula VARCHAR(255) NOT NULL,
    url_foto_74x100 VARCHAR(255) NOT NULL,
    curriculo VARCHAR(255) NOT NULL,
    telefones_intituicionais TEXT NOT NULL,
    campus BIGINT NOT NULL,
    funcao TEXT NOT NULL,
    disciplina_ingresso_id BIGINT NULL,
    categoria_id BIGINT NOT NULL
);

ALTER SEQUENCE servidores_id_seq owned
	BY servidores.id;

ALTER TABLE
    servidores ADD PRIMARY KEY(id);
-- -- -- -- -- -- -- -- -- 
CREATE SEQUENCE disciplinas_id_seq;

CREATE TABLE disciplinas(
    id BIGINT NOT NULL default nextval('disciplinas_id_seq'),
    nome VARCHAR(255) NOT NULL,
    carga_horaria INTEGER NOT NULL,
    codigo CHAR(8) NOT NULL,
    curso_id BIGINT NOT NULL
);

ALTER SEQUENCE disciplinas_id_seq owned
	BY disciplinas.id;

ALTER TABLE
    disciplinas ADD PRIMARY KEY(id);
-- -- -- -- -- -- -- -- -- 

ALTER TABLE
    servidores ADD CONSTRAINT servidores_disciplina_ingresso_id_foreign FOREIGN KEY(disciplina_ingresso_id) REFERENCES disciplinas(id);
ALTER TABLE
    cargos_docente ADD CONSTRAINT cargos_docente_setor_id_foreign FOREIGN KEY(setor_id) REFERENCES setores(id);
ALTER TABLE
    cargos_docente ADD CONSTRAINT cargos_docente_cargo_id_foreign FOREIGN KEY(cargo_id) REFERENCES cargos(id);
ALTER TABLE
    servidores ADD CONSTRAINT servidores_categoria_id_foreign FOREIGN KEY(categoria_id) REFERENCES categorias(id);
ALTER TABLE
    cargos ADD CONSTRAINT cargos_jornada_trabalho_id_foreign FOREIGN KEY(jornada_trabalho_id) REFERENCES jornada_trabalho(id);
ALTER TABLE
    servidores ADD CONSTRAINT servidores_campus_foreign FOREIGN KEY(campus) REFERENCES campi(id);
ALTER TABLE
    cargos_docente ADD CONSTRAINT cargos_docente_docente_id_foreign FOREIGN KEY(docente_id) REFERENCES servidores(id);
ALTER TABLE
    setores ADD CONSTRAINT setores_campus_foreign FOREIGN KEY(campus) REFERENCES campi(id);
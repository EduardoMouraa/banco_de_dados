
create sequence campi_id_seq;

CREATE TABLE "campi"(
    "id" BIGINT NOT NULL default nextval('campi_id_seq'),
    "sigla" CHAR(5) NOT NULL
);

alter sequence campi_id_seq owned
	by campi.id;

ALTER TABLE
    "campi" ADD PRIMARY KEY("id");
-- -- -- -- -- -- -- -- -- 

create sequence cargos_docente_id_seq;

CREATE TABLE "cargos_docente"(
    "id" BIGINT NOT NULL default nextval('cargos_docente_id_seq'),
    "funcao_id" BIGINT NOT NULL,
    "cargo_id" BIGINT NOT NULL,
    "docente_id" BIGINT NOT NULL
);

alter sequence cargos_docente_id_seq owned
	by cargos_docente.id;

ALTER TABLE
    "cargos_docente" ADD PRIMARY KEY("id");
	
-- -- -- 
create sequence setores_id_seq;

CREATE TABLE "setores"(
    "id" BIGINT NOT NULL default nextval('setores_id_seq'),
    "nome" VARCHAR(255) NOT NULL,
    "campus" BIGINT NOT NULL
);

alter sequence setores_id_seq owned
	by setores.id;

ALTER TABLE
    "setores" ADD PRIMARY KEY("id");
-- -- -- 
create sequence cursos_id_seq;
	
CREATE TABLE "cursos"(
    "id" BIGINT NOT NULL default nextval('cursos_id_seq'),
    "nome" BIGINT NOT NULL
);

alter sequence cursos_id_seq owned
	by cursos.id;

ALTER TABLE
    "cursos" ADD PRIMARY KEY("id");

-- -- -- 
create sequence curso_docente_id_seq;

CREATE TABLE "curso_docente"(
    "id" BIGINT NOT NULL default nextval('curso_docente_id_seq'),
    "docente_id" BIGINT NOT NULL,
    "curso_id" BIGINT NOT NULL
);

alter sequence curso_docente_id_seq owned
	by curso_docente.id;

ALTER TABLE
    "curso_docente" ADD PRIMARY KEY("id");
	
-- -- -- 
create sequence cargos_id_seq;

CREATE TABLE "cargos"(
    "id" BIGINT NOT NULL default nextval('cargos_id_seq'),
    "nome" VARCHAR(255) NOT NULL,
    "categoria" CHAR(50) NOT NULL,
    "jornada_trabalho" INTEGER NOT NULL,
    "semanal" BOOLEAN NOT NULL,
    "dedicacao_exclusiva" BOOLEAN NOT NULL
);

alter sequence cargos_id_seq owned
	by cargos.id;

ALTER TABLE
    "cargos" ADD PRIMARY KEY("id");

-- -- -- 
create sequence disciplinas_docente_id_seq;

CREATE TABLE "disciplinas_docente"(
    "id" BIGINT NOT NULL default nextval('disciplinas_docente_id_seq'),
    "disciplina" BIGINT NOT NULL,
    "docente_id" BIGINT NOT NULL
);

alter sequence disciplinas_docente_id_seq owned
	by disciplinas_docente.id;

ALTER TABLE
    "disciplinas_docente" ADD PRIMARY KEY("id");

-- -- -- 
create sequence docente_docente_id_seq;

CREATE TABLE "docente"(
    "id" BIGINT NOT NULL default nextval('docente_docente_id_seq'),
    "nome" VARCHAR(255) NOT NULL,
    "matricula" VARCHAR(255) NOT NULL,
    "url_foto_74x100" VARCHAR(255) NOT NULL,
    "curriculo" VARCHAR(255) NOT NULL,
    "telefones_intituicionais" TEXT NOT NULL,
    "campus" BIGINT NOT NULL
);

alter sequence docente_docente_id_seq owned
	by docente.id;

ALTER TABLE
    "docente" ADD PRIMARY KEY("id");

-- -- -- 

create sequence funcoes_setor_id_seq;

CREATE TABLE "funcoes_setor"(
    "id" BIGINT NOT NULL default nextval('funcoes_setor_id_seq'),
    "setor_id" BIGINT NOT NULL,
    "nome" VARCHAR(255) NOT NULL
);

alter sequence funcoes_setor_id_seq owned
	by funcoes_setor.id;

ALTER TABLE
    "funcoes_setor" ADD PRIMARY KEY("id");

-- -- -- 
create sequence disciplinas_setor_id_seq;

CREATE TABLE "disciplinas"(
    "id" BIGINT NOT NULL default nextval('disciplinas_setor_id_seq'),
    "nome" VARCHAR(255) NOT NULL,
    "carga_horaria" INTEGER NOT NULL,
    "codigo" CHAR(8) NOT NULL,
    "curso_id" BIGINT NOT NULL
);

alter sequence disciplinas_setor_id_seq owned
	by disciplinas.id;

ALTER TABLE
    "disciplinas" ADD PRIMARY KEY("id");
-- -- -- 
	
ALTER TABLE
    "disciplinas_docente" ADD CONSTRAINT "disciplinas_docente_disciplina_foreign" FOREIGN KEY("disciplina") REFERENCES "disciplinas"("id");
ALTER TABLE
    "cargos_docente" ADD CONSTRAINT "cargos_docente_cargo_id_foreign" FOREIGN KEY("cargo_id") REFERENCES "cargos"("id");
ALTER TABLE
    "curso_docente" ADD CONSTRAINT "curso_docente_curso_id_foreign" FOREIGN KEY("curso_id") REFERENCES "cursos"("id");
ALTER TABLE
    "curso_docente" ADD CONSTRAINT "curso_docente_docente_id_foreign" FOREIGN KEY("docente_id") REFERENCES "docente"("id");
ALTER TABLE
    "docente" ADD CONSTRAINT "docente_campus_foreign" FOREIGN KEY("campus") REFERENCES "campi"("id");
ALTER TABLE
    "funcoes_setor" ADD CONSTRAINT "funcoes_setor_setor_id_foreign" FOREIGN KEY("setor_id") REFERENCES "setores"("id");
ALTER TABLE
    "cargos_docente" ADD CONSTRAINT "cargos_docente_funcao_id_foreign" FOREIGN KEY("funcao_id") REFERENCES "funcoes_setor"("id");
ALTER TABLE
    "cargos_docente" ADD CONSTRAINT "cargos_docente_docente_id_foreign" FOREIGN KEY("docente_id") REFERENCES "docente"("id");
ALTER TABLE
    "setores" ADD CONSTRAINT "setores_campus_foreign" FOREIGN KEY("campus") REFERENCES "campi"("id");
ALTER TABLE
    "disciplinas" ADD CONSTRAINT "disciplinas_curso_id_foreign" FOREIGN KEY("curso_id") REFERENCES "cursos"("id");
ALTER TABLE
    "disciplinas_docente" ADD CONSTRAINT "disciplinas_docente_docente_id_foreign" FOREIGN KEY("docente_id") REFERENCES "docente"("id");
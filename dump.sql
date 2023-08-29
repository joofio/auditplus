CREATE TABLE entry (

nummecanografico INT not null,
hora_entrada timestamp not null,
hora_saida timestamp,
local_picagem VARCHAR(20) not null,
PRIMARY KEY (nummecanografico, hora_entrada,local_picagem)
);

CREATE TABLE raw (

nummecanografico INT not null,
resultado VARCHAR(1) not null,
localpicagem VARCHAR(20) not null,
datahora timestamp not null,
PRIMARY KEY (nummecanografico, resultado,localpicagem,datahora)

);
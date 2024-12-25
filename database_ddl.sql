-- area_code_2024 表
CREATE TABLE area_code_2024 (
    code       BIGINT                  NOT NULL,
    name       CHARACTER VARYING(128) NOT NULL DEFAULT '',
    level      SMALLINT               NOT NULL,
    pcode      BIGINT,
    category   INTEGER,
    CONSTRAINT pk_area_code_2024 PRIMARY KEY (code)
);

-- data_sources 表
CREATE TABLE data_sources (
    id          INTEGER                NOT NULL,
    name        CHARACTER VARYING(100) NOT NULL,
    type        CHARACTER VARYING(50)  NOT NULL,
    description TEXT,
    CONSTRAINT pk_data_sources PRIMARY KEY (id)
);

-- disaster_data 表
CREATE TABLE disaster_data (
    id                    CHARACTER VARYING(36)  NOT NULL,
    province              CHARACTER VARYING(50)  NOT NULL,
    city                  CHARACTER VARYING(50)  NOT NULL,
    town                  CHARACTER VARYING(50)  NOT NULL,
    village               CHARACTER VARYING(50)  NOT NULL,
    disaster_category     TEXT                   NOT NULL,
    upload_date           TIMESTAMP WITHOUT TIME ZONE,
    update_date           TIMESTAMP WITHOUT TIME ZONE,
    uploader_id           INTEGER,
    source_id             INTEGER,
    "timestamp"           TIMESTAMP WITHOUT TIME ZONE,
    expiry_date           TIMESTAMP WITHOUT TIME ZONE,
    street                CHARACTER VARYING(50),
    source                CHARACTER VARYING(50),
    carrier               CHARACTER VARYING(50),
    disaster_subcategory  CHARACTER VARYING(50)  NOT NULL,
    disaster_indicator    CHARACTER VARYING(50),
    data_path             TEXT,
    CONSTRAINT pk_disaster_data PRIMARY KEY (id)
);

-- log 表
CREATE TABLE log (
    id         INTEGER                 NOT NULL,
    user_id    INTEGER                 NOT NULL,
    action     CHARACTER VARYING(50)  NOT NULL,
    table_name CHARACTER VARYING(50)  NOT NULL,
    "timestamp" TIMESTAMP WITHOUT TIME ZONE,
    details    TEXT,
    CONSTRAINT pk_log PRIMARY KEY (id)
);

-- user 表
CREATE TABLE "user" (
    id            CHARACTER VARYING(255) NOT NULL,
    username      CHARACTER VARYING(80)  NOT NULL,
    email         CHARACTER VARYING(120) NOT NULL,
    password_hash CHARACTER VARYING(128) NOT NULL,
    role          CHARACTER VARYING(20),
    created_at    TIMESTAMP WITHOUT TIME ZONE,
    updated_at    TIMESTAMP WITHOUT TIME ZONE,
    CONSTRAINT pk_user PRIMARY KEY (id)
);
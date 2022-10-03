-- User Table
CREATE TABLE public.users
(
    id uuid NOT NULL,
    first_name varchar NOT NULL,
    last_name varchar,
    email varchar NOT NULL,
    phone varchar,
    photo varchar,
    gender varchar,
    PRIMARY KEY (id),
    CONSTRAINT email_unique UNIQUE (email)
);

ALTER TABLE IF EXISTS public.users
    OWNER to postgres;


-- USER META Data Table
CREATE TABLE public.user_meta
(
    id bigserial NOT NULL,
    user_id uuid NOT NULL,
    title varchar,
    street varchar,
    city varchar,
    state varchar,
    country varchar,
    postcode varchar,
    latitude numeric DEFAULT 0,
    longitude numeric DEFAULT 0,
    timezone varchar,
    timezone_offset varchar,
    dob date,
    age numeric,
    picture varchar,
    nationality varchar,
    PRIMARY KEY (id),
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

ALTER TABLE IF EXISTS public.user_meta
    OWNER to postgres;
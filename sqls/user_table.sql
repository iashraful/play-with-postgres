-- User Table
CREATE TABLE public.users
(
    id uuid NOT NULL,
    first_name character NOT NULL,
    last_name character,
    email character NOT NULL,
    phone character,
    photo character,
    gender character,
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
    title character,
    street character,
    city character,
    state character,
    country character,
    postcode character,
    latitude numeric DEFAULT 0,
    longitude numeric DEFAULT 0,
    timezone character,
    timezone_offset character,
    dob date,
    age numeric,
    picture character,
    nationality character,
    PRIMARY KEY (id),
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

ALTER TABLE IF EXISTS public.user_meta
    OWNER to postgres;
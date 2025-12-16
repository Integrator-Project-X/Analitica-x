-- Crear schema analytics
CREATE SCHEMA IF NOT EXISTS analytics;

-- ------------------------------------------------------
-- Dimensión de Usuarios
-- ------------------------------------------------------
CREATE OR REPLACE VIEW analytics.v_dim_users AS
SELECT
    u.id_user,
    u.full_name,
    u.age,
    u.address,
    u.phone_number,
    u.identification_number,
    u."isActive",
    u.id_gender,
    g.name AS gender_name,
    u."createdAt" AS created_at,
    u."updatedAt" AS updated_at
FROM public.users u
LEFT JOIN public.genders g ON u.id_gender = g.id_gender;

-- ------------------------------------------------------
-- Dimensión de Mascotas
-- ------------------------------------------------------
CREATE OR REPLACE VIEW analytics.v_dim_pets AS
SELECT
    p.id_pet,
    p.pet_name,
    p.birth_date,
    p."isActive",
    p.id_race,
    r.race_name,
    p.id_animal,
    a.animal_name,
    p."createdAt" AS created_at,
    p."updatedAt" AS updated_at
FROM public.pets p
LEFT JOIN public.race r ON p.id_race = r.id_race
LEFT JOIN public.animals a ON p.id_animal = a.id_animal;

-- ------------------------------------------------------
-- Dimensión de Clínicas
-- ------------------------------------------------------
CREATE OR REPLACE VIEW analytics.v_dim_clinics AS
SELECT
    c.id_clinic,
    c.clinic_name,
    c.address,
    c.phone_number,
    c.identification_number,
    c."isActive",
    c."createdAt" AS created_at,
    c."updatedAt" AS updated_at
FROM public.clinic c;

-- ------------------------------------------------------
-- Dimensión de Tipos de Servicio
-- ------------------------------------------------------
CREATE OR REPLACE VIEW analytics.v_dim_services AS
SELECT
    t.id,
    t.name AS service_name,
    t."is_Active",
    t."created_at" AS created_at,
    t."updated_at" AS updated_at
FROM public.appointments_types t;

-- ------------------------------------------------------
-- Dimensión de Estados de Citas
-- ------------------------------------------------------
CREATE OR REPLACE VIEW analytics.v_dim_status AS
SELECT
    s.id_appointment_status,
    s.status_name,
    s."isActive",
    s."createdAt" AS created_at,
    s."updatedAt" AS updated_at
FROM public.appointment_statuses s;

-- ------------------------------------------------------
-- Fact Table de Citas
-- ------------------------------------------------------
CREATE OR REPLACE VIEW analytics.v_fact_appointments AS
SELECT
    a.id AS appointment_id,
    a.description,
    a."isActive" AS appointment_active,
    a."createdAt" AS created_at,
    a."updatedAt" AS updated_at,
    a.id_pet,
    p.pet_name,
    a.id_user,
    u.full_name AS user_name,
    a.id_diagnosis,
    d.description AS diagnosis_description,
    a.id_type,
    t.name AS service_name,
    a.id_status,
    s.status_name,
    a.id_clinic,
    c.clinic_name,
    a.amount
FROM public.appointments a
LEFT JOIN public.pets p ON a.id_pet = p.id_pet
LEFT JOIN public.users u ON a.id_user = u.id_user
LEFT JOIN public.diagnosis d ON a.id_diagnosis = d.id_diagnosis
LEFT JOIN public.appointments_types t ON a.id_type = t.id
LEFT JOIN public.appointment_statuses s ON a.id_status = s.id_appointment_status
LEFT JOIN public.clinic c ON a.id_clinic = c.id_clinic;

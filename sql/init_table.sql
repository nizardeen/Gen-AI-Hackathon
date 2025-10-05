DROP TABLE IF EXISTS patient_record;

CREATE TABLE IF NOT EXISTS patient_record
(
    patient_id character varying(10) NOT NULL,
    age integer,
    gender character varying(10),
    weight_kg numeric(5,2),
    height_cm numeric(5,2),
    bmi numeric(5,2),
    chronic_conditions text,
    drug_allergies text,
    genetic_disorders text,
    diagnosis text,
    symptoms text,
    recommended_medication text,
    dosage character varying(50),
    duration character varying(50),
    treatment_effectiveness character varying(50),
    adverse_reactions text,
    recovery_time_days integer,
    CONSTRAINT patient_record_pkey PRIMARY KEY (patient_id),
    CONSTRAINT patient_record_age_check CHECK (age >= 0),
    CONSTRAINT patient_record_gender_check CHECK (gender::text = ANY (ARRAY['Male', 'Female', 'Other']::text[])),
    CONSTRAINT patient_record_weight_kg_check CHECK (weight_kg > 0),
    CONSTRAINT patient_record_height_cm_check CHECK (height_cm > 0),
    CONSTRAINT patient_record_bmi_check CHECK (bmi > 0),
    CONSTRAINT patient_record_recovery_time_days_check CHECK (recovery_time_days >= 0)
);
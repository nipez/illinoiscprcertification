-- Add request_type for onsite vs individual quote forms
ALTER TABLE quotes ADD COLUMN request_type TEXT;

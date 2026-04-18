-- ============================================================
-- CampusTrade — Initial Database Schema
-- Run this in the Supabase SQL Editor (Dashboard → SQL Editor)
-- ============================================================

-- ────────────────────────────────────────────────────────────
-- 0. Extensions
-- ────────────────────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


-- ════════════════════════════════════════════════════════════
-- 1. PROFILES
-- ════════════════════════════════════════════════════════════
-- Every Supabase auth user gets a matching profile row.
-- No .edu restriction — any email provider is accepted.
-- ────────────────────────────────────────────────────────────

CREATE TABLE public.profiles (
    id          UUID PRIMARY KEY REFERENCES auth.users (id) ON DELETE CASCADE,
    full_name   TEXT        NOT NULL DEFAULT '',
    avatar_url  TEXT,
    bio         TEXT        DEFAULT '',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE  public.profiles           IS 'Public profile linked 1-to-1 with auth.users.';
COMMENT ON COLUMN public.profiles.id        IS 'Matches auth.users.id — set by trigger, not by client.';
COMMENT ON COLUMN public.profiles.full_name IS 'Display name shown on listings and messages.';

-- Indexes
CREATE INDEX idx_profiles_full_name ON public.profiles USING gin (to_tsvector('english', full_name));

-- RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Profiles are publicly readable"
    ON public.profiles FOR SELECT
    USING (true);

CREATE POLICY "Users can insert their own profile"
    ON public.profiles FOR INSERT
    WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update their own profile"
    ON public.profiles FOR UPDATE
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);


-- ════════════════════════════════════════════════════════════
-- 2. CATEGORIES  (hierarchical taxonomy)
-- ════════════════════════════════════════════════════════════
-- parent_id = NULL → top-level category
-- parent_id = <uuid> → sub-category
-- ────────────────────────────────────────────────────────────

CREATE TABLE public.categories (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        TEXT        NOT NULL,
    slug        TEXT        NOT NULL UNIQUE,
    description TEXT        DEFAULT '',
    parent_id   UUID        REFERENCES public.categories (id) ON DELETE SET NULL,
    sort_order  INT         NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE  public.categories             IS 'Hierarchical product/service taxonomy.';
COMMENT ON COLUMN public.categories.parent_id   IS 'NULL = root category; otherwise points to parent.';
COMMENT ON COLUMN public.categories.slug        IS 'URL-friendly unique identifier (e.g. "textbooks").';

-- Indexes
CREATE INDEX idx_categories_parent  ON public.categories (parent_id);
CREATE INDEX idx_categories_slug    ON public.categories (slug);

-- RLS — categories are read-only for everyone (admins manage via Dashboard)
ALTER TABLE public.categories ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Categories are publicly readable"
    ON public.categories FOR SELECT
    USING (true);


-- ════════════════════════════════════════════════════════════
-- 3. LISTINGS  (items for sale)
-- ════════════════════════════════════════════════════════════

CREATE TYPE public.listing_status AS ENUM ('draft', 'active', 'sold', 'archived');
CREATE TYPE public.listing_condition AS ENUM ('new', 'like_new', 'good', 'fair', 'poor');

CREATE TABLE public.listings (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    seller_id       UUID            NOT NULL REFERENCES public.profiles (id) ON DELETE CASCADE,
    category_id     UUID            NOT NULL REFERENCES public.categories (id) ON DELETE RESTRICT,
    title           TEXT            NOT NULL,
    description     TEXT            NOT NULL DEFAULT '',
    price           NUMERIC(10, 2)  NOT NULL CHECK (price >= 0),
    condition       public.listing_condition NOT NULL DEFAULT 'good',
    status          public.listing_status    NOT NULL DEFAULT 'active',
    images          TEXT[]          DEFAULT '{}',
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT now()
);

COMMENT ON TABLE  public.listings             IS 'Items listed for sale by students.';
COMMENT ON COLUMN public.listings.seller_id   IS 'FK → profiles.id of the seller.';
COMMENT ON COLUMN public.listings.images      IS 'Array of Supabase Storage URLs.';

-- Indexes
CREATE INDEX idx_listings_seller    ON public.listings (seller_id);
CREATE INDEX idx_listings_category  ON public.listings (category_id);
CREATE INDEX idx_listings_status    ON public.listings (status);
CREATE INDEX idx_listings_search    ON public.listings USING gin (
    to_tsvector('english', title || ' ' || description)
);

-- RLS
ALTER TABLE public.listings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Active listings are publicly readable"
    ON public.listings FOR SELECT
    USING (status = 'active' OR auth.uid() = seller_id);

CREATE POLICY "Authenticated users can create listings"
    ON public.listings FOR INSERT
    WITH CHECK (auth.uid() = seller_id);

CREATE POLICY "Sellers can update their own listings"
    ON public.listings FOR UPDATE
    USING (auth.uid() = seller_id)
    WITH CHECK (auth.uid() = seller_id);

CREATE POLICY "Sellers can delete their own listings"
    ON public.listings FOR DELETE
    USING (auth.uid() = seller_id);


-- ════════════════════════════════════════════════════════════
-- 4. ASKS  (buy / want requests)
-- ════════════════════════════════════════════════════════════

CREATE TYPE public.ask_status  AS ENUM ('open', 'fulfilled', 'closed');
CREATE TYPE public.ask_urgency AS ENUM ('low', 'medium', 'high');

CREATE TABLE public.asks (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    requester_id    UUID            NOT NULL REFERENCES public.profiles (id) ON DELETE CASCADE,
    category_id     UUID            NOT NULL REFERENCES public.categories (id) ON DELETE RESTRICT,
    title           TEXT            NOT NULL,
    description     TEXT            NOT NULL DEFAULT '',
    budget_max      NUMERIC(10, 2)  CHECK (budget_max IS NULL OR budget_max >= 0),
    urgency         public.ask_urgency  NOT NULL DEFAULT 'medium',
    status          public.ask_status   NOT NULL DEFAULT 'open',
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT now()
);

COMMENT ON TABLE  public.asks                IS 'Buy-requests posted by students looking for items.';
COMMENT ON COLUMN public.asks.requester_id   IS 'FK → profiles.id of the requester.';
COMMENT ON COLUMN public.asks.budget_max     IS 'Maximum the requester is willing to pay (nullable = no limit).';

-- Indexes
CREATE INDEX idx_asks_requester ON public.asks (requester_id);
CREATE INDEX idx_asks_category  ON public.asks (category_id);
CREATE INDEX idx_asks_status    ON public.asks (status);
CREATE INDEX idx_asks_search    ON public.asks USING gin (
    to_tsvector('english', title || ' ' || description)
);

-- RLS
ALTER TABLE public.asks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Open asks are publicly readable"
    ON public.asks FOR SELECT
    USING (status = 'open' OR auth.uid() = requester_id);

CREATE POLICY "Authenticated users can create asks"
    ON public.asks FOR INSERT
    WITH CHECK (auth.uid() = requester_id);

CREATE POLICY "Requesters can update their own asks"
    ON public.asks FOR UPDATE
    USING (auth.uid() = requester_id)
    WITH CHECK (auth.uid() = requester_id);

CREATE POLICY "Requesters can delete their own asks"
    ON public.asks FOR DELETE
    USING (auth.uid() = requester_id);


-- ════════════════════════════════════════════════════════════
-- 5. AUTO-CREATE PROFILE TRIGGER
-- ════════════════════════════════════════════════════════════
-- Fires after a new row is added to auth.users (on sign-up).
-- Pulls full_name from user_metadata if provided, otherwise
-- falls back to the email prefix.
-- ────────────────────────────────────────────────────────────

CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    INSERT INTO public.profiles (id, full_name, avatar_url)
    VALUES (
        NEW.id,
        COALESCE(
            NEW.raw_user_meta_data ->> 'full_name',
            split_part(NEW.email, '@', 1)
        ),
        NEW.raw_user_meta_data ->> 'avatar_url'
    );
    RETURN NEW;
END;
$$;

-- Attach the trigger to the Supabase auth.users table
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_new_user();


-- ════════════════════════════════════════════════════════════
-- 6. UPDATED_AT AUTO-REFRESH TRIGGER
-- ════════════════════════════════════════════════════════════
-- Reusable function: auto-sets updated_at = now() on UPDATE.
-- ────────────────────────────────────────────────────────────

CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

CREATE TRIGGER set_profiles_updated_at
    BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER set_listings_updated_at
    BEFORE UPDATE ON public.listings
    FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER set_asks_updated_at
    BEFORE UPDATE ON public.asks
    FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


-- ════════════════════════════════════════════════════════════
-- 7. SEED DATA — Default Categories
-- ════════════════════════════════════════════════════════════

INSERT INTO public.categories (name, slug, description, sort_order) VALUES
    ('Textbooks',    'textbooks',    'Course textbooks and study materials',     1),
    ('Electronics',  'electronics',  'Laptops, phones, calculators, etc.',       2),
    ('Furniture',    'furniture',    'Dorm and apartment furniture',             3),
    ('Clothing',     'clothing',     'Apparel, shoes, and accessories',          4),
    ('Tickets',      'tickets',      'Event and transportation tickets',         5),
    ('Services',     'services',     'Tutoring, moving help, and freelance',     6),
    ('Other',        'other',        'Everything else',                          99);

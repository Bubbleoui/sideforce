-- À coller une seule fois dans Supabase > SQL Editor > Run

create table if not exists public.allowed_emails (email text primary key);
insert into public.allowed_emails (email) values ('costalucas13011@gmail.com') on conflict do nothing;
alter table public.allowed_emails enable row level security;   -- aucune policy : illisible depuis l'appli

create table if not exists public.items (
  collection text not null,
  id text not null,
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (collection, id)
);
alter table public.items enable row level security;
alter table public.items replica identity full;

create or replace function public.is_member() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.allowed_emails where lower(email) = lower(coalesce(auth.jwt() ->> 'email', '')))
$$;
grant execute on function public.is_member() to authenticated;

drop policy if exists members_all on public.items;
create policy members_all on public.items for all to authenticated
  using (public.is_member()) with check (public.is_member());

create or replace function public.patch_item(c text, i text, p jsonb) returns void
language sql security invoker as $$
  update public.items set data = data || p, updated_at = now() where collection = c and id = i
$$;
grant execute on function public.patch_item(text, text, jsonb) to authenticated;

-- synchro en direct
do $$ begin
  alter publication supabase_realtime add table public.items;
exception when duplicate_object then null; end $$;

-- images des réfs
insert into storage.buckets (id, name, public) values ('refs', 'refs', true) on conflict (id) do nothing;
drop policy if exists refs_insert on storage.objects;
create policy refs_insert on storage.objects for insert to authenticated
  with check (bucket_id = 'refs' and public.is_member());
drop policy if exists refs_delete on storage.objects;
create policy refs_delete on storage.objects for delete to authenticated
  using (bucket_id = 'refs' and public.is_member());

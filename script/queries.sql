-- Top 10 games which are free and have the most positive_ratings
select name
from asteam
where positive_ratings - negative_ratings > 0 and price = 0
order by positive_ratings - negative_ratings desc limit 10;

-- name of games that have same name registered by more than one developer
select name, count(name) from asteam group by name having count(name) > 1 order by count desc;

-- games made for adults
select name, required_age from asteam where required_age >=18;

-- game selected on their category
select name from asteam where 'Online Multi-Player' = any(categories);

-- gives the name and mb of ram required by the pc for game
create or replace function spec2(integer)
  returns table(name text, hd int) as
  $$
    select name, $1 as hd
    from asteam, requirementsdata
    where steam_appid = appid and pc_requirements like concat(concat('%', $1),'mb ram%');
  $$
  language sql ;

select name, regexp_matches(linux_requirements, '%_GB Hard Drive Space%', 'g')
from asteam, requirementsdata
where steam_appid = appid and linux_requirements like '%_GB Hard Drive Space%' limit 3;




--
create or replace function spec(i integer)
  returns table(name text, hd integer) as
  $$
      select asteam.name, i as hd
      from asteam, requirementsdata
      where steam_appid = appid and linux_requirements like concat(concat('%', i),'GB Hard Drive Space%');
  $$
language plpgsql;

-- achha walax
create function spec(integer)
  returns table(name text, hd int) as
  $$
    select name, $1 as hd
    from asteam, requirementsdata
    where steam_appid = appid and linux_requirements like concat(concat('%', $1),'GB Hard Drive Space%');
  $$
  language plpgsql ;

create or replace function spec1(X integer)
  returns table(name text, hd integer) as
  $$
   with recursive cte(name, i) as (select spec(i) union select spec(i+1) where i < 16) select * from cte;
  $$
language sql;

create or replace function spec1(X integer)
  returns table(name text, hd integer) as
  $$
   with recursive cte(name, X) as (select spec(X) union select cte(name, X+1) where i < 16) select * from cte;
    -- declare
    --   i integer := 0;
    --   s table := select spec(X)
    -- begin
    --   for i in (X+1).. 16 loop
    --     s := s union select spec(i);
    --   end loop;
    -- end;
  $$
language sql;








































-------
-- to filter out games based on their genres
select name, genres from asteam where 'Early Access' = any(genres);

-- to filter out games based on given developer
select distinct(developer) from asteam;

-- to filter out the given operating system
select name, platforms from asteam where 'windows' = any(platforms);

--
create view platforms as (select platforms from asteam);

drop view platforms;


-- all the genres of games
create view genre as select distinct(genres) from (select unnest(genres) as genres from asteam) as t;
drop view genre;
-- top 10 genres
select genre, count(genre) from (select unnest(genres) as genre from asteam) as t group by genre order by count desc limit 10;

-- all the of the games
select distinct(categories) from (select unnest(categories) as categories from asteam) as t;

-- popular tags
select steamspy_tags, count(steamspy_tags) from (select unnest(steamspy_tags) as steamspy_tags from asteam) as t group by steamspy_tags order by count desc limit 10;

-- total no. of times a tag is talked about
select sum(a25d), sum(a1980s) from steamspytagdata ;


-- controller games    vr     new releases    upcomming    top sellers     recomendationsq

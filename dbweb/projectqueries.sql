-- 1. How old is the Game--
--select * from release_date(2011);--
create or replace function release_date(integer) 
returns table(game text, num date) as 
$$
select name, release_date
from asteam 
where cast(extract(year from release_date) as integer) = $1
order by release_date desc
-- (2020 - cast(extract(year from release_date) as integer)) 
$$
LANGUAGE sql;

-- 2. Names of game from given developer--
--select * from developers_game('Gearbox Software');--
create or replace function developers_game(text)
returns table(game text) as
$$
select name
from asteam
where lower(developer) = lower($1)
$$
LANGUAGE sql;


-- 3 games with given developer and year--
--select dev_release_date('valve', 2016)--
create or replace function dev_release_date(text, integer)
returns table(game text, num date) as
$$
select d.game, num  
from developers_game($1) as d, release_date($2) as r 
where d.game = r.game 
order by num desc;
$$
LANGUAGE sql;


--4 Search by platform --
--select * from platform('windows');--
create or replace function platform(text)
returns table(game text) as
$$
select name 
from asteam 
where Array[lower($1)] <@ platforms;
$$
LANGUAGE sql;


--5 If boughtornot and inornot both false then delete that row from the cart table --
--update cart set boughtornot = False where userid ='aaditya';--

create or replace function bot()
returns trigger as
$$
    begin
        if ((new.incartornot = new.boughtornot) and (new.incartornot = false or new.boughtornot = false)) then
            delete from cart where userid = old.userid;
        end if;
        return NEW;
    end;
$$
LANGUAGE plpgsql;

create trigger removerow
after update
on cart
for each row 
execute procedure bot(); 

--view for adding commutative entries and userid, userid--
create or replace view arefriends as 
select userid1, userid2 
from friends 
union 
select userid2, userid1 
from friends
union 
select userid1, userid1 from friends;

--view to find all the people in the same component--
create or replace view potentialfriendsview
as with recursive ctepath 
as (
    (select * from arefriends) 
    union 
    (select arefriends.userid1, ctepath.userid2 
        from arefriends, ctepath 
        where arefriends.userid2 = ctepath.userid1)) 
    select * from ctepath;


--all the people in the same component are potential friends--
create or replace function potentialfriends(text)
returns table(username text) as
$$
select distinct userid2 
from potentialfriendsview
where lower(userid1) = lower($1) and lower(userid2) != lower($1)
$$
language sql;

create or replace function myfriend(text)
returns table(usernames text) as
$$
select userid2 from arefriends where lower(userid1) = lower($1) and userid1 != userid2
$$
language sql;

--recommended games that a friend plays but a user doesn't--
create or replace function recommendfromfriend(text)
returns table(game integer) as
$$
(select distinct appid from myfriend($1), cart where myfriend = userid) 
except 
(select appid from cart where lower(userid) = lower($1));
$$
language sql;


--recommended top games from other component--
create or replace function recommendfromothercomp(text)
returns table(game integer) as
$$
--should be from asteam--
(select appid from cart)

except

((select appid from potentialfriends($1), cart where username = userid)
union
(select appid from cart where lower(userid) = lower($1)))
$$
language sql;


--display a string like the game entered--
create or replace function games(text)
returns table(game text, genre text[], cost float) as
$$
begin
return query
select name, genres, price from asteam where lower(name) like concat(lower($1),'%');
end;
$$
language plpgsql;
